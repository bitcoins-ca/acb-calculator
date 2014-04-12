
import contextlib
import psycopg2,psycopg2.extras
   
   
   
   
def connect():
    connection =psycopg2.connect(database='gains')
    
    try:
        psycopg2.extras.register_hstore(connection)
    except Exception, e:
        print 'warning, hstore not yet installed!'
    
    return connection



#I think psycopg now implements this pattern for us, although only in version2.5+ which I don't currently have.
#clever use of schema could really help here.
@contextlib.contextmanager
def dbcontext(schema=None,commit=True):
    conn=connect()
    cursor=conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if(schema):
        cursor.execute("SET search_path TO %s" % schema)
    yield cursor
    if(commit):
        conn.commit()
    cursor.close()
    conn.close()

