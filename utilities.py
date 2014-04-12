# Modified from
# https://wiki.python.org/moin/PythonDecoratorLibrary
import functools

def memoize(f):
    cache={}
    @functools.wraps(f)
    def wrapped(*args):
        if args not in cache:
            cache[args]=f(*args)
        return cache[args]
    return wrapped
    
