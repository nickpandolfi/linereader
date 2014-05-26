__author__ = 'Nicholas C Pandolfi'

import os

class ClosedError(Exception):
    '''
    This error is called when the user tries to
    access methods or attributes from a close file
    '''
    pass


def addspace(string, targetlen):
    string += ' ' * (targetlen - len(string))
    return string

def removespace(string):
    return int(string.strip())

def checkdate(odir, tdir, accept = None, reject = None, absent = None):
    if not os.path.exists(odir):
        raise FileExistsError('Original directory must exist to perform a checkDate')
    if os.path.exists(tdir):
        if os.path.getmtime(odir) > os.path.getmtime(tdir):
            if reject: reject()
        else:
            if accept: accept()
    else:
        if absent: absent()