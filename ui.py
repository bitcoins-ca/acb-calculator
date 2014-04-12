import logging,os,shutil
from uuid import UUID

import bottle
import pandas
from bottle import Bottle, run, request,response, static_file,redirect

from cStringIO import StringIO
import session, database,config, utilities

logging.basicConfig(filename=config.LOGFILE_PATH,level=logging.DEBUG,format='%(asctime)s: %(filename)s:%(lineno)d:%(levelname)s:%(message)s')

bottle.TEMPLATE_PATH.insert(0,config.TEMPLATE_PATH)

app=Bottle()

app.add_hook('before_request',session.load)
app.add_hook('after_request',session.save)


from view_helpers import view

CSV_FILE_NAMES=["trade_history.csv","order_history.csv","account_history.csv"]

class UploadSet:
    def __init__(self,uuid):
        self.uuid = UUID(uuid)
       
       
    @property
    def directoryPath(self):
        return os.path.join(config.UPLOAD_DIRECTORY,str(self.uuid))
    def ensureDirectoryExists(self):
        if not self.directoryExists():
            os.mkdir(self.directoryPath)
        
    def directoryExists(self):
        return os.path.isdir(self.directoryPath)

    def files(self):
        return {name: os.path.exists(os.path.join(self.directoryPath, name))
                for name in CSV_FILE_NAMES}
       
    def deleteAllFiles(self):
        shutil.rmtree(self.directoryPath)
    
    @utilities.memoize
    def transactions(self):
        path=os.path.join(self.directoryPath, 'account_history.csv')
        frame =  pandas.read_csv(path).sort_index(axis=0, ascending=False)
        return frame[frame["Date/Time"].notnull()].rename(columns={"Date/Time":"Date"})

    @utilities.memoize
    def depositsCAD(self):
        columns=['Date', 'Change(CAD)','Total(CAD)' ]
        frame=self.transactions()
        condition = (frame["Type"]=="deposit") & (frame['Change(CAD)'].notnull())
        return frame[condition][columns]
        
        
    @utilities.memoize
    def depositsBTC(self):
        columns=['Date','Change(BTC)','Total(BTC)'  ]
        frame=self.transactions()
        condition = (frame["Type"]=="deposit") & (frame['Change(BTC)'].notnull())
        return frame[condition][columns]
        
        
    def calculated(self):
        assert 0, "shane needs to fix this"
        import calculator
        return calculator.CostBaseCalculator(self.directoryPath)

    @utilities.memoize
    def withdrawalsCAD(self):
        columns=['Date','Change(CAD)','Total(CAD)']
        frame=self.transactions()
        condition = (frame["Type"]=="withdrawal") & (frame['Change(CAD)'].notnull())
        return frame[condition][columns]
        
    @utilities.memoize
    def withdrawalsBTC(self):
        columns=['Date','Change(BTC)','Total(BTC)','wallet']
        frame=self.transactions()
        condition = (frame["Type"]=="withdrawal") & (frame['Change(BTC)'].notnull())
        
        return frame[condition][columns]
        
    @utilities.memoize
    def fees(self):
        columns=['Date','Change(BTC)','Total(BTC)','Change(CAD)','Total(CAD)']
        frame=self.transactions()
        return frame[frame["Type"]=="fee"][columns]

    
        
    def chart(self,column):
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
        from matplotlib.figure import Figure
        
        fig = Figure(figsize=(14,6))
        canvas = FigureCanvas(fig)
        fig.set_canvas(canvas)
        ax = fig.add_subplot(111)
        
        
        series = self.transactions().set_index('Date')[column] 
        series.plot(ax=ax)
        fig.autofmt_xdate()
        io = StringIO()
        fig.savefig(io, format='svg')
        return io.getvalue()


@app.get('/api/data')
def data():
    uuid=session.session()['upload_uuid']
    uploadSet=UploadSet(uuid)
    return uploadSet.transactions()['Total(BTC)'].to_json(orient='values')
################################################################################
# Routes                                                                       #
################################################################################
@app.get('/')
@view('index')
def index():
    assert os.path.isdir(config.UPLOAD_DIRECTORY)
    uuid=session.session()['upload_uuid']
    uploadSet=UploadSet(uuid)
    return locals()
    

@app.post('/')
def post_index():
    uuid=session.session()['upload_uuid']
    uploadSet=UploadSet(uuid)
    count=0
    for name in CSV_FILE_NAMES:
        if name in request.files:
            f = request.files[name]
            if f.filename!=name:
                session.setErrorMessage("'%s' is probably not the file you mean"%f.filename)
                redirect('/')
            uploadSet.ensureDirectoryExists()
            path=os.path.join(config.UPLOAD_DIRECTORY,str(uuid), name)
            f.save(file(path,'wc'))
            count+=1

    session.setInfoMessage(str(count) + " files provided")
    
    redirect('/')

@app.post('/delete_uploads')
def delete_uploads():
    uuid=session.session()['upload_uuid']
    uploadSet=UploadSet(uuid)
    uploadSet.deleteAllFiles()
    session.setErrorMessage("Files Deleted")
    redirect('/')
    
@app.get('/upload/<upload_uuid>')
def returning_user(upload_uuid):
    session.setInfoMessage("Hello, welcome back")
    session.session()['upload_uuid']=upload_uuid
    redirect('/')
     
@app.get('/tax_info')
@view('tax_info')
def tax_info():
    return {}
            
   
