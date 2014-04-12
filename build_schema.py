'''
    utility script to initialize sqlite database.
    Do we even need security on the HRDR?
'''
from database import dbcontext
import sys,subprocess
import optparse

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-c", "--create", dest="create",action="store_true",help="destroy/create database", metavar="CREATE")


if __name__=="__main__":

    (options, args) = parser.parse_args()
    
    if options.create:
        print 'creating database'
        try:
            subprocess.check_output(["dropdb","gains"])
        except:
            pass
        subprocess.check_output(["createdb","gains"])
    
    
    schema=file('schema.sql').read() 

    with dbcontext() as cursor:
        cursor.execute(schema)
