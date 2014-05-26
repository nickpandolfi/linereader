__author__ = 'Nicholas C Pandolfi'


#The MIT License (MIT)
#
#Copyright (c) 2014 Nicholas C Pandolfi
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


'''
Reads randomly accessed lines from a text file faster than Python\'s built-in linecache,
and creates dynamic data types for the manipulation of massive data sets.
'''


from .c_reader import copen
from .d_reader import dopen
from .lrcompiler import construct, visconstruct, precompile, stackcompile, dircompile
from .lrcompiler import load, build, cachebuild, cnlcount, getline, getonce, clearcache

#initial commit

#Add all files to initiate the project

#polymorphesized copen and dopen, removed cython libraries,
#multithreaded a precompiler, added extra utility functions
