from functools import wraps
import time

__author__ = 'fangshi'


def profile(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        ts = time.time()
        result = fn(*args, **kwargs)
        te = time.time()
        print '\n'
        print '-' * 38, 'profile', '-' * 37
        print "function = {0}".format(fn.__name__)
        doc = fn.__doc__
        if doc:
            doc = doc.strip()
            print "doc      = {0}".format(doc)
        print "time     = %.6f ms" % ((te-ts) * 1000)
        # print "res      = %s" % (result)
        print '-' * 40, 'ok', '-' * 40
        return result
    return wrapper
