from __future__ import absolute_import, division, print_function

import OpenGL
from OpenGL import GL, arrays

from ..utilities import Unspecified, specified, getspecified

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
        self._divisor = None
    
    @property
    def type(self):
        return self._type
        
    @property
    def size(self):
        return self._size
        
    @property
    def divisor(self):
        return self._divisor
    
    def set_data(self, data, size, usage=DEFAULT_BUFFER_USAGE):
        type = types.gltype(data)
        GL.glBufferData(self._target, size, data, usage)
        self._type = type
        self._size = size
        
    def get_sub_data(self, data, size, offset=0):
        #type = types.gltype(data) #TODO: Type Check?
        GL.glGetBufferSubData(self._target, offset, size, arrays.ArrayDatatype.voidDataPointer(data))
    
    def set_sub_data(self, data, size, offset=0):
        #type = types.gltype(data) #TODO: Type Check?
        GL.glBufferSubData(self._target, offset, size, arrays.ArrayDatatype.voidDataPointer(data))
    
    def bind_base(self, index, target=Unspecified):
        target = getspecified(target, self._target)
        GL.glBindBufferBase(target, index, self._handle)

class ArrayBuffer(Buffer):
    _target = GL.GL_ARRAY_BUFFER

class ElementArrayBuffer(Buffer):
    _target = GL.GL_ELEMENT_ARRAY_BUFFER
   
class UniformBuffer(Buffer):   
    _target = GL.GL_UNIFORM_BUFFER

class TransformFeedbackBuffer(Buffer):
    _target = GL.GL_TRANSFORM_FEEDBACK_BUFFER

VertexArrayObject = VertexArray
VertexBufferObject = ArrayBuffer
IndexBufferObject = ElementArrayBuffer