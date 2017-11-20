import contextlib as cl

from .. import utilities


class Handle(metaclass=utilities.UniversalMethodMeta):
    _null = 0
    @utilities.universalmethod
    def create(cls, obj):
        assert bool(obj) == False
        obj._value = cls._create()
        return obj
    @utilities.universalmethod
    def delete(cls, obj):
        assert bool(obj) == True
        cls._delete(obj._value)
        obj._value = cls._null
        return obj
    @utilities.universalmethod
    def bind(cls, obj):
        pass
    @utilities.universalmethod
    def unbind(cls, obj):
        pass
    def __init__(self, value=None):
        self._value = self._null if value is None else value
    def __bool__(self):
        return bool(self._value != self._null)
    def __eq__(self, other):
        return self._value == other._value
    def __ne__(self, other):
        return not self == other
    def __int__(self):
        return int(self._value)
    def __str__(self):
        return "{}({})".format(type(self).__name__, self._value)


@cl.contextmanager
def scoped(obj, cls=None):
    cls = type(obj) if cls is None else cls
    try:
        cls.create(obj)
        yield obj
    finally:
        cls.delete(obj)


@cl.contextmanager
def bound(obj, cls=None):
    cls = type(obj) if cls is None else cls
    try:
        cls.bind(obj)
        yield obj
    finally:
        cls.unbind(obj)


@cl.contextmanager
def mapped(obj, cls=None):
    cls = type(obj) if cls is None else cls
    try:
        cls.map(obj)
        yield obj
    finally:
        cls.unmap(obj)
