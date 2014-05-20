__author__ = 'Nicholas C Pandolfi'

import os
import sys
from .lrbuilder import cachebuild
from .lrtools import ClosedError

class copen(object):
    def __init__(self, file, overwrite = False):
        object.__init__(self)
        self.current = 1
        self.filename = file
        self.lines, self.__cache = cachebuild(file, overwrite)
    
    def __del__(self):
        del self.__cache
    
    def __getattr__(self, attr):
        if attr == '_copen__cache':
            raise ClosedError('Operations cannot be done on a closed file')
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format('copen', attr))
    
    def __len__(self):
        return os.path.getsize(self.filename) + int(self.lines)
    
    def __bool__(self):
        return bool(len(self))
    
    def __contains__(self, item):
        return item in self.__cache
    
    def __iter__(self):
        lines = self.lines
        cache = self.getcache()
        for count in cache:
            yield count
    
    def __sizeof__(self):
        memory = 0
        for item in dir(self):
            memory += sys.getsizeof(eval('self.{}'.format(item)))
        return memory
    
    def readline(self):
        line = self.__cache[self.current - 1]
        self.current += 1
        return line
    
    def seekline(self, line):
        self.current = line
    
    def readlines(self):
        return self.__cache

    def getline(self, number):
        return self.__cache[number - 1]
    
    def getlines(self, start, stop):
        return self.__cache[start - 1 : stop]
    
    def readnext(self, number):
        selection = self.__cache[self.current - 1 : self.current + number - 1]
        self.current += number
        return selection
    
    def wrapcache(self):
        return lambda number: self.__cache[number - 1]
    
    def getcache(self):
        return self.__cache
    
    def storecache(self):
        global cache
        cache[self.filename] = self.__cache
    
    def close(self):
        del self.__cache
