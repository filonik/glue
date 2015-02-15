from __future__ import absolute_import, division, print_function

import OpenGL
from OpenGL import GL

from . import resources, types

DEFAULT_BUFFER_USAGE = GL.GL_STATIC_DRAW

class VertexArray(resources.GLResource):
    @classmethod
    def bind(cls, obj):
        GL.glBindVertexArray(cls.handle(obj))
    
    def __init__(self, *args, **kwargs):
        super(VertexArray, self).__init__(*args, **kwargs)
        
    @classmethod
    def create_handle(self):
        return GL.glGenVertexArrays(1)
    
    @classmethod
    def delete_handle(cls, handle):
        GL.glDeleteVertexArrays(handle)

class Buffer(resources.GLResource):
    _target = None
    
    @classmethod
    def bind(cls, obj):
        GL.glBindBuffer(cls._target, cls.handle(obj))
    
    @classmethod
    def create_handle(self):
        return GL.glGenBuffers(1)
    
    @classmethod
    def delete_handle(cls, handle):
        GL.glDeleteBuffers(handle)
    
    def __init__(self, *args, **kwargs):
        super(Buffer, self).__init__(*args, **kwargs)
        self._type = None
    
    @property
    def type(self):
        return self._type
    
    def set_data(self, data, size, usage=DEFAULT_BUFFER_USAGE):
        type = types.gltype(data)
        GL.glBufferData(self._target, size, data, usage)
        self._type = type
        
    def set_sub_data(self, data, size, offset=0):
        type = types.gltype(data)
        GL.glBufferSubData(self._target, offset, size, data)

class ArrayBuffer(Buffer):
    _target = GL.GL_ARRAY_BUFFER

class ElementArrayBuffer(Buffer):
    _target = GL.GL_ELEMENT_ARRAY_BUFFER

VertexArrayObject = VertexArray
VertexBufferObject = ArrayBuffer
IndexBufferObject = ElementArrayBuffer