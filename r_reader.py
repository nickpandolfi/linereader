__author__ = 'Nicholas C Pandolfi'

import os
import sys
from .lrbuilder import objbuild
from .lrtools import ClosedError

class ropen(object):
    def __init__(self, file):
        object.__init__(self)
        self.filename = file
        self.file, self.__ref = objbuild(self.filename)
        self.file.seek(0)
    
    def __del__(self):
        self.file.close()
        del self.__ref
    
    def __getattr__(self, attr):
        if attr == '_ropen__ref':
            raise ClosedError('Operations cannot be done on a closed file')
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format('ropen', attr))
    
    def __len__(self):
        return os.path.getsize(self.filename)
    
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
    
    def seekline(self, number):
        self.file.seek(self.__ref[number - 1])

    def getline(self, number):
        self.file.seek(self.__ref[number - 1])
        return self.file.readline()
    
    def getlines(self, start, stop):
        self.file.seek(self.__ref[start - 1])
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