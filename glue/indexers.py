import collections

from .utilities import compose

# Provide uniform access to attrs, items, fields etc.

class Indexer(collections.MutableMapping):
    def __init__(self, obj, cls, name, fget=None, fset=None, fdel=None, fitr=None, flen=None):
        self.obj = obj
        self.cls = cls
        self.name = name
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.fitr = fitr
        self.flen = flen
    def __getitem__(self, key):
        return self.fget(self.obj, key)
    def __setitem__(self, key, value):
        self.fset(self.obj, key, value)
    def __delitem__(self, key):
        self.fdel(self.obj, key)
    def __contains__(self, key):
        try:
            self[key]
        except (AttributeError, KeyError, IndexError, TypeError):
            return False
        else:
            return True
    def __iter__(self):
        return self.fitr(self.obj)
    def __len__(self):
        return self.flen(self.obj)
    def __repr__(self):
        return '%s{%s.%s}' % (self.__class__.__name__, self.cls.__name__, self.name)

def getitem(obj, key):
    return obj[key]

def setitem(obj, key, value):
    obj[key] = value

def delitem(obj, key):
    del obj[key]

def itritems(obj):
    try:
        return iter(obj)
    except TypeError:
        return iter(())

def lenitems(obj):
    try:
        return len(obj)
    except TypeError:
        return 0

itrattrs = compose(iter, dir)
lenattrs = compose(len, dir)

def attrindexer(obj):
    return Indexer(obj, type(obj), 'attrs', getattr, setattr, delattr, itrattrs, lenattrs)

def itemindexer(obj):
    return Indexer(obj, type(obj), 'items', getitem, setitem, delitem, itritems, lenitems)