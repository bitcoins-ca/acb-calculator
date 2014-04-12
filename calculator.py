
import pandas,os
from numpy import isnan

def acb(sorted_events_frame, btc_balance):
    frame = sorted_events_frame.copy()
    #assert "Date" in frame
    #assert "Traded Amount" in frame
    #assert "Traded Currency" in frame
    #assert "For Amount" in frame
    #assert "For Currency" in frame
    #assert "Exchange Rate" in frame
    acb = 0
    last_average_acb = 0
    cad_balance = 0
    average_acb = 0
    action = ""
    #frame["acb"] = pandas.Series(index=frame.index)
    out = []
    for index, row in frame.iterrows():
        acb_delta = 0
        btc_amount = 0
        cad_amount = 0
        action = ""
        used_last_average = False
        
        if row["Type"] == "deposit":
            # Exchange rate is not provided for deposits.
            if not isnan(row["Change(BTC)"]):
                row["Exchange Rate"] = last_average_acb
                used_last_average = True
                action = "BTC deposit"
                btc_amount = row["Change(BTC)"]
                acb_delta = 0
            elif not isnan(row["Change(CAD)"]):
                row["Exchange Rate"] = ""
                action = "CAD deposit"
                cad_amount = row["Change(CAD)"]
                acb_delta = row["Change(CAD)"]
            else:
                assert 0

        if row["Type"] == "withdrawal":
            # Exchange rate is not provided for withdrawals.
            if not isnan(row["Change(BTC)"]):
                row["Exchange Rate"] = last_average_acb
                used_last_average = True
                action = "BTC withdrawal"
                btc_amount = row["Change(BTC)"]
                acb_delta = 0
            elif not isnan(row["Change(CAD)"]):
                row["Exchange Rate"] = ""
                action = "CAD withdrawal"
                cad_amount = row["Change(CAD)"]
                acb_delta = row["Change(CAD)"]
            else:
                assert 0

        if row["Type"] == "fee":
            # Exchange rate is not provided for fees.
            row["Exchange Rate"] = last_average_acb
            used_last_average = True
            if not isnan(row["Change(BTC)"]):
                action = "BTC fee"
                btc_amount = row["Change(BTC)"]
                acb_delta = 0
            elif not isnan(row["Change(CAD)"]):
                action = "CAD fee"
                cad_amount = row["Change(CAD)"]
                acb_delta = row["Change(CAD)"]
            else:
                assert 0

        if row["Type"] == "trade":
            if row["Traded Currency"] == "CAD":
                cad_amount = -row["Traded Amount"]
                if row["For Currency"] == "BTC":
                    btc_amount = row["For Amount"]
                    action = "Bought BTC with CAD"
                    acb_delta = row["Traded Amount"]
            elif row["Traded Currency"] == "BTC":
                btc_amount = -row["Traded Amount"]
                if row["For Currency"] == "CAD":
                    cad_amount = row["For Amount"]
                    action = "Sold BTC for CAD"
                    # Use the current (as of last purchase) acb to value the BTC that we've disposed of.
                    # Not the selling price or exchange rate!
                    acb_delta = (btc_amount * average_acb)
            else:
                assert 0
                
        #assert not (acb_delta is None)
        
        if used_last_average:
            average_acb = last_average_acb
        else:
            if btc_balance <> 0:
                average_acb = acb / btc_balance
            else:
                #print "Zero!"
                average_acb = 0

        btc_balance = btc_balance + btc_amount
        acb = acb + acb_delta
        last_average_acb = average_acb

        yield {"Index":index, "Type":row["Type"], "Date":row["Date"], "Action": action, "CAD Change":cad_amount, "ACB Change":acb_delta, 
               "ACB":acb, "BTC Change":btc_amount, 
               "BTC Balance":btc_balance, "BTC Price":row["Exchange Rate"], "Per-BTC ACB":average_acb, "Wallet": row["wallet"]}
    
    

def CostBaseCalculator(directory):
    
    
    # Files are in reverse chronological order. Sort in chronological order.
    trans =pandas.read_csv(os.path.join(directory,'account_history.csv')).sort_index(axis=0, ascending=False) # better than (by="Date/Time")
    orders=pandas.read_csv(os.path.join(directory,'order_history.csv'))  .sort_index(axis=0, ascending=False) # better than (by="Created")
    trades=pandas.read_csv(os.path.join(directory,'trade_history.csv'))  .sort_index(axis=0, ascending=False) # better than (by="Processed")
    
    
    trans = trans[trans["Date/Time"].notnull()].rename(columns={"Date/Time":"Date"})
    orders = orders[orders["Created"].notnull()].rename(columns={"Created":"Date"})
    trades = trades[trades["Processed"].notnull()].rename(columns={"Processed":"Date"})
    trades["Type"] = "trade"
    
    fees = trans[trans["Type"]=="fee"]
    fees = fees[["Date","Type","Change(BTC)","Change(CAD)"]]
    
    withdrawals = trans[trans.Type=="withdrawal"]
    deposits = trans[trans["Type"]=="deposit"]
    
    fills = orders[orders["Status"]=="filled"]
    fills = fills[["Completed","Status","Remaining","Total","Rate","Exchange","Requested","Value"]].rename(columns={"Completed":"Date"})
    df = pandas.concat([fees,trades,deposits,withdrawals], keys=["fees","trades","deposits","withdrawals"])
    
    df = df.sort_index(by="Date")
    
    frame = pandas.DataFrame(list(acb(df,45.15)),  #pay no attention to the man behind the curtain.
        columns=["Date","Type","Action","CAD Change","ACB Change","ACB","BTC Change","BTC Balance","BTC Price","Per-BTC ACB"])
    
    return frame
    
