__author__ = 'Nicholas C Pandolfi'

import os
import sys
from .lrcompiler import construct, load, build, BUFFERSIZE
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
    
    def __call__(self, line):
        return self.getline(line)
    
    def __getitem__(self, line):
        return self.getline(line)
    
    def __getattr__(self, attr):
        if attr == '_dopen__ref':
            raise ClosedError('Operations cannot be done on a closed file')
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format('dopen', attr))
    
    def __loadsetup(self):
        maxlength = len(open(self.dirname).readline())
        dirname = self.filename[:self.filename.index('.')] + '.lrdict'
        self.file = open(self.filename)
        self.__ref = load(dirname, maxlength)

    def __buildsetup(self):
        self.file = open(self.filename)
        self.__ref = build(self.filename)
    
    def __len__(self):
        return os.path.getsize(self.filename)
    
    def __bool__(self):
        return bool(len(self))
    
    def __iter__(self):
        return iter(open(self.filename))
    
    def __next__(self):
        return self.file.readline()
    
    def __sizeof__(self):
        memory = 0
        for item in dir(self):
            memory += sys.getsizeof(eval('self.{}'.format(item)))
        return memory
    
    def count(self, item, buffer = BUFFERSIZE):
        leftoff = self.file.tell()
        self.file.seek(0)
        reps = 0
        content = True
        while content:
            content = file.read(buffer)
            reps += content.count(item)
        self.file.seek(leftoff)
        return reps
    
    def seekline(self, number):
        try:
            self.file.seek(self.__ref(number))
            return number - previous
        except ValueError:
            raise ValueError('line number \'{}\' does not exist'.format(number))

    def getline(self, number):
        try:
            self.file.seek(self.__ref(number))
            return self.file.readline()
        except ValueError:
            raise ValueError('line number \'{}\' does not exist'.format(number))
    
    def read(self, chars = None):
        return self.file.read(chars)
    
    def readline(self):
        return self.file.readline()
    
    def readlines(self):
        lines = self.file.readlines()
        return lines
    
    def readnext(self, number):
        lines = [self.readline() for x in range(number)]
        return lines
    
    def seek(self, pos, whence = 0):
        previous = self.file.tell()
        self.file.seek(pos, whence)
        return pos - previous
    
    def getlines(self, start, stop):
        try:
            self.file.seek(self.__ref(start))
            lines = [self.readline() for x in range(start, stop + 1)]
            return lines
        except ValueError:
            raise ValueError('line number \'{}\' does not exist'.format(start))
    
    def getref(self):
        return self.__ref
    
    def tell(self):
        return self.file.tell()
    
    def resetpointer(self):
        self.file.seek(0)
    
    def close(self):
        self.file.close()
        del self.__ref
