__author__ = 'Nicholas C Pandolfi'

import os
import sys
from .lrbuilder import construct, load, build
from .lrtools import ClosedError, checkdate

class dopen(object):
    def __init__(self, file):
        object.__init__(self)
        self.filename = file
        self.dirname = file[:file.index('.')] + '.lrdict'
        checkdate(self.filename, self.dirname,
                  accept = self.__loadsetup,
                  reject = self.__buildsetup,
                  absent = self.__buildsetup)
    
    def __del__(self):
        self.file.close()
        del self.__ref
    
    def __getattr__(self, attr):
        if attr == '_dopen__ref':
            raise ClosedError('Operations cannot be done on a closed file')
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format('dopen', attr))
    
    def __loadsetup(self):
        maxlength = len(open(self.dirname).readline())
        dirname = self.filename[:self.filename.index('.')] + '.lrdict'
        self.file, self.__ref = open(self.filename), load(dirname, maxlength)

    def __buildsetup(self):
        self.file, self.__ref = open(self.filename), build(self.filename)
    
    def __len__(self):
        return os.path.getsize(self.filename)# + len(self.__ref)
    
    def __bool__(self):
        return bool(len(self))
    
    def __iter__(self):
        return iter(open(self.filename))
    
    def __next__(self):
        return next(self.file)
    
    def __sizeof__(self):
        memory = 0
        for item in dir(self):
            memory += sys.getsizeof(eval('self.{}'.format(item)))
        return memory
    
    def seekline(self, number):
        self.file.seek(self.__ref(number))

    def getline(self, number):
        self.file.seek(self.__ref(number))
        return self.file.readline()
    
    def read(self, chars):
        return self.file.read(chars)
    
    def readline(self):
        return self.file.readline()
    
    def readlines(self):
        lines = self.file.readlines()
        return lines
    
    def readnext(self, number):
        lines = [self.readline() for x in range(number)]
        return lines
    
    def seek(self, pos):
        self.file.seek(pos)
    
    def getlines(self, start, stop):
        self.file.seek(self.__ref(start))
        lines = [self.readline() for x in range(start, stop + 1)]
        return lines
    
    def getref(self):
        return self.__ref
    
    def tell(self):
        return self.file.tell()
    
    def resetpointer(self):
        self.file.seek(0)
    
    def close(self):
        self.file.close()
        del self.__ref