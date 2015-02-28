from __future__ import absolute_import, division, print_function

import collections
import contextlib as cl

import six

from clibs import glfw3 as GLFW

from ..flyweights import Resource
from ..utilities import chdir, Unspecified, specified, getspecified

def initialize():
    GLFW.initialize()
    
    from ..gl import gl
    gl._set_backend('glfw')

def terminate():
    GLFW.terminate()

@cl.contextmanager
def initialized():
    initialize()
    try:
        yield
    finally:
        terminate()

class Context(Resource):
    __references = dict()
    
    @classmethod
    def references(cls, context=Unspecified):
        return cls.__references
    
    @classmethod
    def create_handle(cls, window):
        return window.context
    
    @classmethod
    def delete_handle(cls, handle):
        pass
    
    @classmethod
    def get_current(cls):
        handle = GLFW.Context.get_current()
        return cls(handle=handle)
    
    @classmethod
    def set_current(cls, context):
        GLFW.Context.set_current(context._handle)
    
    def __init__(self, *args, **kwargs):
        super(Context, self).__init__(*args, **kwargs)
        
        self._references = collections.defaultdict(dict)
    
    def dispose(self):
        for cls in self._references:
            references = self._references[cls]
            for handle, reference in list(six.iteritems(references)):
                del references[handle]
                cls.delete(handle)
        
        super(Context, self).dispose()
