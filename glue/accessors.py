from builtins import hasattr, getattr, setattr, delattr
from operator import attrgetter, itemgetter

from . import utilities


AttrErrors = (TypeError, AttributeError)
ItemErrors = (TypeError, KeyError, IndexError)

iterattrs = utilities.compose(iter, dir)
lenattrs = utilities.compose(len, dir)


def hasitem(obj, key):
    try:
        obj[key]
    except ItemErrors:
        return False
    else:
        return True


def getitem(obj, key, default=utilities.Unspecified):
    if utilities.specified(default):
        try:
            return obj[key]
        except ItemErrors:
            return default
    else:
        return obj[key]


def setitem(obj, key, value):
    obj[key] = value


def delitem(obj, key):
    try:
        del obj[key]
    except ItemErrors:
        pass


def iteritems(obj):
    try:
        return iter(obj)
    except TypeError:
        return iter(())


def lenitems(obj):
    try:
        return len(obj)
    except TypeError:
        return 0
