import OpenGL
from OpenGL import GL

from .. import utilities

from . import handles


class VertexArray(handles.Handle):
    @classmethod
    def _create(cls):
        return GL.glGenVertexArrays(1)
    @classmethod
    def _delete(cls, value):
        GL.glDeleteVertexArrays(value)
    @utilities.universalmethod
    def bind(cls, obj):
        GL.glBindVertexArray(obj._value)
    @utilities.universalmethod
    def unbind(cls, obj):
        GL.glBindVertexArray(obj._null)


class Buffer(handles.Handle):
    _type = None
    @classmethod
    def _create(cls):
        return GL.glGenBuffers(1)
    @classmethod
    def _delete(cls, value):
        GL.glDeleteBuffers(1, GL.GLuint(value))
    @utilities.universalmethod
    def bind(cls, obj):
        GL.glBindBuffer(cls._type, obj._value)
    @utilities.universalmethod
    def unbind(cls, obj):
        GL.glBindBuffer(cls._type, obj._null)
    @utilities.universalmethod
    def bind_base(cls, obj, index):
        GL.glBindBufferBase(cls._type, index, obj._value)
    @utilities.universalmethod
    def unbind_base(cls, obj, index):
        GL.glBindBufferBase(cls._type, index, obj._null)
    @utilities.universalmethod
    def data(cls, obj, data, size, usage=GL.GL_STATIC_DRAW):
        GL.glBufferData(cls._type, size, data, usage)
    @utilities.universalmethod
    def sub_data(cls, obj, data, size, offset=0):
        GL.glBufferSubData(cls._type, offset, size, data)


class ArrayBuffer(Buffer):
    _type = GL.GL_ARRAY_BUFFER

class ElementArrayBuffer(Buffer):
    _type = GL.GL_ELEMENT_ARRAY_BUFFER

class TransformFeedbackBuffer(Buffer):
    _type = GL.GL_TRANSFORM_FEEDBACK_BUFFER

class UniformBuffer(Buffer):
    _type = GL.GL_UNIFORM_BUFFER

class ShaderStorageBuffer(Buffer):
    _type = GL.GL_SHADER_STORAGE_BUFFER

class DrawIndirectBuffer(Buffer):
    _type = GL.GL_DRAW_INDIRECT_BUFFER


VertexBuffer = ArrayBuffer
IndexBuffer = ElementArrayBuffer
