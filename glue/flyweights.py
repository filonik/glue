import weakref

import six

from .utilities import identity, Unspecified, specified, getspecified

def getdefault(references, handle, default=None):
    try:
        return references[handle]()
    except KeyError:
        return default

class FlyweightMeta(type):
    def __call__(cls, *args, **kwargs):
        context = kwargs.get('context', Unspecified)
        handle = kwargs.get('handle', Unspecified)
        
        references = cls.references(context=context)
        
        if not specified(handle):
            handle = cls.create_handle(*args, **kwargs)
        
        result = getdefault(references, handle)
        
        if result is None:
            result = super(FlyweightMeta, cls).__call__(handle=handle, context=context)
            references[handle] = weakref.ref(result)
        
        return result

@six.add_metaclass(FlyweightMeta)
class Resource(object):
    _zero_handle = None
    
    @classmethod
    def references(cls, context=Unspecified):
        raise NotImplementedError
    
    @classmethod
    def handle(cls, obj):
        return cls._zero_handle if obj is None else obj._handle
    
    @classmethod
    def create_handle(cls):
        return cls._zero_handle
    
    @classmethod
    def delete_handle(cls, handle):
        pass
    
    @classmethod
    def cleanup(cls, context=Unspecified):
        references = cls.references(context=context)
        
        for handle, reference in list(six.iteritems(references)):
            if reference() is None:
                del references[handle]
                cls.delete_handle(handle)
    
    def __init__(self, *args, **kwargs):
        self._context = kwargs.pop('context', Unspecified)
        self._handle = kwargs.pop('handle', Unspecified)
        super(Resource, self).__init__(*args, **kwargs)
    
    def __nonzero__(self):
        return self._handle != self._zero_handle
    
    __bool__ = __nonzero__
    
    def dispose(self, context=Unspecified):
        references = self.references(context=context)
        
        del references[self._handle]
        self.delete_handle(self._handle)
        
        self._handle = self._zero_handle