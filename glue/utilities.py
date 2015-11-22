from __future__ import absolute_import, division, print_function

import functools as ft
import itertools as it

import six

def identity(obj):
    return obj

def compose2(f, g):
    return lambda *args, **kwargs: f(g(*args, **kwargs))

def compose(*fs):
    return ft.reduce(compose2, fs)

def nth(iterable, n, default=None):
    return next(it.islice(iterable, n, None), default)

class Undefined(object):
    def __nonzero__(self): return False
    def __repr__(self): return "Undefined"
Undefined = Undefined()

class Unspecified(object):
    def __nonzero__(self): return False
    def __repr__(self): return "Unspecified"
Unspecified = Unspecified()

def defined(obj):
    return obj is not Undefined
    
def specified(obj):
    return obj is not Unspecified
    
def getdefined(obj, default=None):
    return obj if defined(obj) else default
    
def getspecified(obj, default=None):
    return obj if specified(obj) else default

def hashable(obj):
    try:
        hash(obj)
    except TypeError:
        return False
    return True

def reversedict(d):
    return dict(map(reversed, six.iteritems(d)))

import contextlib as cl
import os

@cl.contextmanager  
def chdir(dirname=None):  
    curdir = os.getcwd()
    try:  
        if dirname is not None:  
            os.chdir(dirname)  
        yield
    finally:
        os.chdir(curdir)