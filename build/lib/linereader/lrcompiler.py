__author__ = 'Nicholas C Pandolfi'

import os
import sys
from multiprocessing import Process
from .lrtools import addspace, removespace, checkdate
from itertools import islice

BUFFERSIZE = 1024 ** 2

class NotCompiledError(Exception):
    '''
    This error is called when the user tried to load
    from a '.lrdict' file that does not exist yet
    '''
    pass

def construct(filename):
    dirname = os.path.splitext(filename)[0] + '.lrdict'
    dirfile = open(dirname, 'w+')
    file = open(filename)
    maxlength = len(str(os.path.getsize(filename)))
    chars = 0
    
    dirfile.write(addspace('0', maxlength) + '\n')
    
    for (offset, line) in enumerate(file):
        chars += len(line) + 1
        dirfile.write(addspace(str(int(chars)), maxlength) + '\n')
    
    dirfile.close()
    return dirname, int(maxlength + 1)

def visconstruct(filename, increment = 0):
    percent = 0.0
    size = os.path.getsize(filename)
    dirname = os.path.splitext(filename)[0] + '.lrdict'
    dirfile = open(dirname, 'w+')
    file = open(filename)
    maxlength = len(str(os.path.getsize(filename)))
    chars = 0
    
    dirfile.write(addspace('0', maxlength) + '\n')
    
    for (offset, line) in enumerate(file):
        current = round(chars / size * 100, increment)
        if percent != current:
            percent = current
            print('status: {}%'.format(current))
        chars += len(line) + 1
        dirfile.write(addspace(str(int(chars)), maxlength) + '\n')
    
    dirfile.close()
    return dirname, int(maxlength + 1)

def load(dirname, maxlength):
    try:
        file = open(dirname)
    except FileNotFoundError:
        raise NotCompiledError("file '{}' does not exist, original file may need to be compiled first".format(
        dirname))
    
    def ref_function(number):
        file.seek(((number - 1) * maxlength) + (number - 1))
        string = removespace(file.readline()[:-1])
        return string

    return ref_function

def build(filename):
    return load(*construct(filename))

def cnlcount(filename, buffer = BUFFERSIZE):
    file = open(filename)
    newlines = 0
    chars = 0
    content = True
    while content:
        content = file.read(buffer)
        newlines += content.count('\n')
        chars += len(content)
    file.close()
    return {'chars': chars, 'lines': newlines, 'cpl': chars/newlines}

def precompile(filename, newprocess = True):
    if newprocess:
        process = Process(target = construct, args = (filename,))
        process.start()
    else:
        construct(filename)

def stackcompile(filelist, pool = True):
    if pool:
        for filename in filelist:
            precompile(filename, newprocess = True)
    else:
        for filename in filelist:
            precompile(filename, newprocess = False)

def dircompile(directory, supported = [], notcompile = [], pool = True, treecompile = False):
    if not isinstance(supported, list):
        raise ValueError("'supported' parameter must consist of a list of file extensions")
    tocompile = []
    if not treecompile:
        names = (filename for filename in os.listdir(directory))
    else:
        def names():
            for walked in os.walk(directory):
                dirname = walked[0]
                for eachfile in walked[2]:
                    yield os.path.join(dirname, eachfile)
        names = names()
    for filename in names:
        extension = os.path.splitext(filename)[1]
        if (extension in supported) and (filename not in notcompile):
            tocompile.append(os.path.join(directory, filename))
    stackcompile(tocompile, pool)

cache = {} # The global cache if copen is used, else dopen uses handles, and cache remains unused

def cachebuild(filename, overwrite = False):
    global cache
    if filename in cache:
        if overwrite:
            cache[filename] = tuple(open(filename).readlines())
    else:
        cache[filename] = tuple(open(filename).readlines())
    lines = cache[filename]
    return len(lines), lines

def getline(filename, line, reload = False):
    return cachebuild(filename, overwrite = reload)[1][line - 1]

def getonce(filename, linenumber, useislice = True):
    file = open(filename)
    if useislice:
        line = next(islice(file, linenumber - 1, linenumber))
        file.close()
        return line
    else:
        for offset, line in enumerate(file):
            if offset + 1 == linenumber:
                return line

def clearcache(dontclear = []):
    global cache
    todelete = []
    for entry in cache:
        if entry not in dontclear:
            todelete.append(entry)
    for impending in todelete:
        del cache[impending]
