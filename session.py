import database
from bottle import request,response
import logging,json

import uuid

#this needs to be set per-project, probably.
SESSION_COOKIE_NAME='gains.session.uuid'


def createSession():
    with database.dbcontext() as cursor:
        sql="INSERT INTO session DEFAULT VALUES RETURNING uuid"
        cursor.execute(sql)
        uuid=cursor.fetchone()['uuid']
        #Do I need to do this every time?  Or just on createSession
        response.set_cookie(SESSION_COOKIE_NAME,uuid,path="/")
        logging.debug("COOKIE SET :%s",uuid)
        return uuid
        
def load():
    logging.debug("load")
    with database.dbcontext() as cursor:
        session_uuid=request.get_cookie(SESSION_COOKIE_NAME)
        if not session_uuid:
            session_uuid=createSession()
            
        sql="SELECT properties FROM session WHERE uuid=%(session_uuid)s"
        cursor.execute(sql,locals())
        
        row=cursor.fetchone()
        
        if not row:
            logging.debug("NO ROW")
            session_uuid=createSession()
            cursor.execute(sql,locals())
            row=cursor.fetchone()
            
        properties=row['properties']
        assert 'sessionuuid' not in request.environ
        
        if 'upload_uuid' not in properties:
            properties['upload_uuid'] = str(uuid.uuid4())
        
        request.environ['session']=properties
        request.environ['sessionuuid']=session_uuid
    

def save():
 
    logging.debug("%s SAVE SESSION", request.url)
    session_uuid=request.environ.get('sessionuuid')
    if not session_uuid: 
        logging.warning("%s NO SESSION_UUID", request.url)
        return
        
    with database.dbcontext() as cursor:
        sql="UPDATE session SET properties=%(properties)s  WHERE uuid=%(session_uuid)s"
        properties=request.environ['session']
        cursor.execute(sql,locals())
        
def session():
    return request.environ.get('session')
#shouldn't make this DB call every single time!
def user():
    s=session()
    if not s: return
    username= s.get('username')
    if not username:return
        
    sql="""SELECT * FROM gains_user WHERE name=%(username)s"""
    with database.dbcontext() as cursor:
        cursor.execute(sql,locals())
        user=cursor.fetchone()
        if not user:return
        user=dict(user)
        user['created']=str(user['created'])
        return user
        
    
def setErrorMessage(s):
    session()['error']=s
def setInfoMessage(s):
    session()['info']=s