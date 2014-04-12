'''
    Utility functions that will be exposed inside views.
    
    For example, this allows you to write
        <b>Username: {{Helpers().user()}}</b>
    inside a view
'''
import os,bottle
import session
import config


 


def mercurialInfo():
    try:
        import subprocess
        return subprocess.check_output(['hg','parents'],cwd=config.THIS_DIRECTORY)

    except Exception,e:
        return "Couldn't determine repository information" + str(e)
    

# View Helpers #################################################################    
class Helpers:
        
    @staticmethod
    def user():
        return session.user()
    @staticmethod
    def username():
        return session.user()['name']
    @staticmethod
    def test():
        return "test helper method"
        
    @staticmethod
    def error():
        return 'error' in session.session()
        
    @staticmethod
    def info():
        return 'info' in session.session()
        
    @staticmethod
    def upload_uuid():
        return session.session().get('upload_uuid')
        
    @staticmethod
    def config():
        return config
        
    @staticmethod
    def errormessage():
        s=session.session()
        
        error=s.get('error')
        if 'error' in s:
            del s['error']
        return error
        
    @staticmethod
    def infomessage():
        s=session.session()
        info=s.get('info')
        if 'info' in s:
            del s['info']
        return info
           
    @staticmethod
    def mercurialInfo():
        return mercurialInfo()
        
#Our own view handler that jams in extra info
def view(tplName):
    return bottle.view(tplName,Helpers=Helpers)


