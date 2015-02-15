from __future__ import absolute_import, division, print_function

import functools as ft

from .indexers import Indexer

def attrcached(attr):
    def decorator(func):
        @ft.wraps(func)
        def decorated(obj, *args, **kwargs):
            if not hasattr(obj, attr):
                setattr(obj, attr, func(obj, *args, **kwargs))
            return getattr(obj, attr)
        return decorated
    return decorator

def decorationmethod(cls, name=None):
    def decorator(func):
        func_names = [name or func.__name__]
        
        for func_name in func_names:
            old_func = getattr(cls, func_name, None)
            new_func = func(old_func)
            setattr(cls, func_name, new_func)
        
        return func
    return decorator

class IndexedProperty(object):
    _indexer_type = Indexer
            
    def __init__(self, fget=None, fset=None, fdel=None, fitr=None, flen=None, name=None):
        self._name = name
        
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.fitr = fitr
        self.flen = flen
    
    @property
    def name(self):
        return self._name or self.fget.__name__
    
    @property
    def attr(self):
        return '__cached_%s_indexer' % (self.name,)
    
    def __get__(self, obj, cls=None):
        @attrcached(self.attr)
        def _get(obj):
            return self._indexer_type(obj, cls, self.name, self.fget, self.fset, self.fdel, self.fitr, self.flen)
        
        if obj is not None:
            return _get(obj)
        elif cls is not None:
            return self
        else:
            raise ValueError("%s: Cannot get without 'obj' or 'cls'."  % (self,))
    
    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.fitr, self.flen)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.fitr, self.flen)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.fitr, self.flen)
    
    def iterator(self, fitr):
        return type(self)(self.fget, self.fset, self.fdel, fitr, self.flen)
        
    def length(self, flen):
        return type(self)(self.fget, self.fset, self.fdel, self.fitr, flen)

indexedproperty = IndexedProperty

class UniversalMethod(object):
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, cls=None):
        if cls is None:
            cls = type(obj)
        def _f(*args, **kwargs):
            return self.f(cls, obj, *args, **kwargs)
        return _f

class UniversalProperty(object):
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, cls=None):
        if cls is None:
            cls = type(obj)
        return self.f(cls, obj)

universalmethod = UniversalMethod
universalproperty = UniversalProperty
