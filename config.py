
import json,os


THIS_DIRECTORY      = os.path.dirname(__file__)
UPLOAD_DIRECTORY    = "/var/local/gains.bitcoins.ca/uploads"

LOGFILE_PATH        = os.path.join(THIS_DIRECTORY,'gains.log')
TEMPLATE_PATH       = os.path.join(THIS_DIRECTORY,'views')
STATIC_ROOT         = os.path.join(THIS_DIRECTORY,'static')
VERSION             = '0.0.3'
