import types


_UNIVERSAL_METHOD_FLAG = "_isuniversalmethod"


def universalmethod(func):
    result = classmethod(func)
    setattr(result, _UNIVERSAL_METHOD_FLAG, True)
    return result


def isuniversalmethod(func):
    return getattr(func, _UNIVERSAL_METHOD_FLAG, False)


class UniversalMethodMeta(type):
    def __new__(cls, class_name, bases, class_dict):
        result = super().__new__(cls, class_name, bases, class_dict)
        methods = {name: value for name, value in class_dict.items() if isuniversalmethod(value)}
        
        old_init = result.__init__
        
        def new_init(self, *args, **kwargs):
            for name, value in methods.items():
                setattr(self, name, types.MethodType(getattr(type(self), name), self))
            
            old_init(self, *args, **kwargs)
        
        result.__init__ = new_init

        return result


def identity(obj):
    return obj


def compose(*funcs):
    def _compose(f, g):
        return lambda *args, **kwargs: f(g(*args, **kwargs))
    return ft.reduce(_compose, funcs, identity)


def unique_instance(name, truth=True):
    cls = type(name, (object,), {'__bool__': lambda self: truth, '__repr__': lambda self: name, '__str__': lambda self: name})
    return cls()


Unspecified = unique_instance("Unspecified", False)

def specified(obj):
    return obj is not Unspecified

def getspecified(obj, default=None):
    return obj if specified(obj) else default
