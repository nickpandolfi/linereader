__author__ = 'Nicholas C Pandolfi'

import os
import sys
from .lrcompiler import cachebuild, BUFFERSIZE, cache
from .lrtools import ClosedError
from itertools import islice


class copen(object):
    def __init__(self, file, overwrite = False):
        object.__init__(self)
        self.current = 1
        self.filename = file
        self.lines, self.__cache = cachebuild(file, overwrite)
        self.__pointer = 0
        self.chars = os.path.getsize(file) - self.lines
        self.seek(0)
    
    def __call__(self, line):
        return self.getline(line)
    
    def __getitem__(self, line):
        return self.getline(line)
    
    def __getattr__(self, attr):
        if attr in ('_copen__cache', '_copen__chargen'):
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
        for count in self.__cache:
            yield count
    
    def __sizeof__(self):
        memory = 0
        for item in dir(self):
            memory += sys.getsizeof(eval('self.{}'.format(item)))
        return memory
    
    def count(self, item):
        reps = 0
        for line in self.__cache:
            reps += line.count(item)
        return reps
    
    def read(self, chars = None, whole = False):
        if chars:
            string = ''
            for iteration in range(chars):
                try:
                    string += next(self.__chargen)
                except StopIteration:
                    return string
            return string
        else:
            if whole:
                return ''.join(self.__cache)
            else:
                string = ''
                for char in self.__chargen:
                    string += char
                return string
    
    def seek(self, pos, whence = 0):
        backup = self.chars
        previous = self.__pointer
        if whence != 0:
            if whence == 1:
                pos += self.__pointer
            elif whence == 2:
                backup = 0
                pos = self.chars - pos
            else:
                raise ValueError("'whence' parameter only accepts values of (0,1,2)")
        chargen = (char for line in self.__cache for char in line)
        try:
            self.__chargen = islice(chargen, pos, None)
        except ValueError:
            self.__chargen = islice(chargen, backup, None)
        self.__pointer = pos
        return pos - previous
    
    def tell(self):
        return self.__pointer
    
    def lineposition(self, number):
        chars = 0
        for line in self.__cache[:number - 1]:
            chars += len(line)
        return chars
    
    def pointerstats(self, chars = None):
        if chars == None:
            return self.pointerstats(self.__pointer)
        passed = 0
        for (offset, line) in enumerate(self.__cache):
            linestart = passed
            for char in line:
                if passed == chars:
                    current = (offset + 1, chars - linestart, passed)
                    break
                passed += 1
            else:
                continue
            break
        try:
            return current
        except UnboundLocalError:
            raise ValueError('character number \'{}\' does not exist'.format(chars))
    
    def syncpointers(self, current_is_dominant = True):
        if current_is_dominant:
            self.seek(self.lineposition(self.current))
        else:
            self.current = self.pointerstats(self.__pointer)[0]
    
    def resetpointer(self):
        self.seek(0)
    
    def readline(self):
        try:
            line = self.__cache[self.current - 1]
            self.current += 1
            return line
        except IndexError:
            return ''
    
    def seekline(self, line):
        if self.getline(line):
            self.current = line
        else:
            self.current = len(self.__cache)
    
    def readlines(self):
        return list(self.__cache)

    def getline(self, number):
        try:
            return self.__cache[number - 1]
        except IndexError:
            return ''
    
    def getlines(self, start, stop):
        return self.__cache[start - 1 : stop]
    
    def readnext(self, number):
        selection = self.__cache[self.current - 1 : self.current + number - 1]
        self.current += number
        return list(selection)
    
    def wrapcache(self):
        return lambda number: self.__cache[number - 1]
    
    def getref(self):
        return self.__cache
    
    def close(self, clearentry = False):
        global cache
        del self.__cache
        del self.__chargen
        if clearentry:
            del cache[self.filename]
