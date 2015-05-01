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
        GL.glDeleteVertexArrays(1, GL.GLuint(handle))

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
        GL.glDeleteBuffers(1, GL.GLuint(handle))
    
    def __init__(self, *args, **kwargs):
        super(Buffer, self).__init__(*args, **kwargs)
        self._type = None
        self._size = None
    
    @property
    def type(self):
        return self._type
    
    def set_data(self, data, size, usage=DEFAULT_BUFFER_USAGE):
        type = types.gltype(data)
        GL.glBufferData(self._target, size, data, usage)
        self._type = type
        self._size = size
        
    def get_sub_data(self, data, size, offset=0):
        #type = types.gltype(data) #TODO: Type Check?
        GL.glGetBufferSubData(self._target, offset, size, data)
    
    def set_sub_data(self, data, size, offset=0):
        #type = types.gltype(data) #TODO: Type Check?
        GL.glBufferSubData(self._target, offset, size, data)
    
    def bind_base(self, index):
        GL.glBindBufferBase(self._target, index, self._handle)
    
class ArrayBuffer(Buffer):
    _target = GL.GL_ARRAY_BUFFER

class ElementArrayBuffer(Buffer):
    _target = GL.GL_ELEMENT_ARRAY_BUFFER
    
class TransformFeedbackBuffer(Buffer):
    _target = GL.GL_TRANSFORM_FEEDBACK_BUFFER

VertexArrayObject = VertexArray
VertexBufferObject = ArrayBuffer
IndexBufferObject = ElementArrayBuffer