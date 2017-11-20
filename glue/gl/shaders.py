import logging

import ctypes

import OpenGL
from OpenGL import GL

from .. import utilities

from . import _raw
from . import handles
from . import types

_logger = logging.getLogger(__name__.split(".").pop())


# Helper Functions (Omitted unused types for brevity...)

INPUT_FUNCTIONS = {
    types.Vec2Type: GL.glVertexAttribPointer,
    types.Vec3Type: GL.glVertexAttribPointer,
    types.Vec4Type: GL.glVertexAttribPointer,
}

UNIFORM_FUNCTIONS = {
    types.ScalarType: GL.glUniform1f,
    types.Vec2Type: GL.glUniform2fv,
    types.Vec3Type: GL.glUniform3fv,
    types.Vec4Type: GL.glUniform4fv,
    types.Mat2Type: GL.glUniformMatrix2fv,
    types.Mat3Type: GL.glUniformMatrix3fv,
    types.Mat4Type: GL.glUniformMatrix4fv,
    types.IScalarType: GL.glUniform1i,
    types.IVec2Type: GL.glUniform2iv,
    types.IVec3Type: GL.glUniform3iv,
    types.IVec4Type: GL.glUniform4iv,
    types.UScalarType: GL.glUniform1ui,
    types.UVec2Type: GL.glUniform2uiv,
    types.UVec3Type: GL.glUniform3uiv,
    types.UVec4Type: GL.glUniform4uiv,
    types.Sampler1DType: GL.glUniform1i,
    types.Sampler2DType: GL.glUniform1i,
    types.Sampler3DType: GL.glUniform1i,
    types.SamplerCubeType: GL.glUniform1i,
}


_noop = lambda *args, **kwargs: None

def input_setter(program, key, type):
    location = GL.glGetAttribLocation(program, key)
    if location == -1:
        _logger.debug('Input "{}" ignored.'.format(key))
        return _noop
    function = INPUT_FUNCTIONS[type]
    _, dtype, shape = type
    def _input_setter(type, value, stride, offset=0, divisor=0):
        GL.glEnableVertexAttribArray(location)
        GL.glBindBuffer(type, value)
        function(location, shape[0], gltype, GL.GL_FALSE, stride, ctypes.c_void_p(int(offset)))
        GL.glVertexAttribDivisor(location, divisor)
        GL.glBindBuffer(type, 0)
    return _input_setter


def uniform_setter(program, key, type):
    location = GL.glGetUniformLocation(program, key)
    if location == -1:
        _logger.debug('Uniform "{}" ignored.'.format(key))
        return _noop
    function = UNIFORM_FUNCTIONS[type]
    _, dtype, shape = type
    return {
        0: lambda value, count=1, transpose=False: function(location, value),
        1: lambda value, count=1, transpose=False: function(location, count, value),
        2: lambda value, count=1, transpose=False: function(location, count, transpose, value)
    }[len(shape)]

    
def uniform_block_setter(program, key):
    index = GL.glGetProgramResourceIndex(program, GL.GL_UNIFORM_BLOCK, key)
    if index == 0xFFFFFFFF:
        _logger.debug('Uniform Block "{}" ignored.'.format(key))
        return _noop
    binding = _raw.glGetProgramResourceiv(program, GL.GL_UNIFORM_BLOCK, index, [GL.GL_BUFFER_BINDING])[0]
    def _uniform_block_setter(buffer):
        buffer.bind_base(binding)
    return _uniform_block_setter


def shader_storage_block_setter(program, key):
    index = GL.glGetProgramResourceIndex(program, GL.GL_SHADER_STORAGE_BLOCK, key)
    if index == 0xFFFFFFFF:
        _logger.debug('Shader Storage Block "{}" ignored.'.format(key))
        return _noop
    binding = _raw.glGetProgramResourceiv(program, GL.GL_SHADER_STORAGE_BLOCK, index, [GL.GL_BUFFER_BINDING])[0]
    def _shader_storage_block_setter(buffer):
        buffer.bind_base(binding)
    return _shader_storage_block_setter


class Shader(handles.Handle):
    _type = None
    @classmethod
    def _create(cls):
        return GL.glCreateShader(cls._type)
    @classmethod
    def _delete(cls, value):
        GL.glDeleteShader(value)
    @classmethod
    def from_type(cls, type, *args, **kwargs):
        return {
            GL.GL_COMPUTE_SHADER: ComputeShader,
            GL.GL_VERTEX_SHADER: VertexShader,
            GL.GL_TESS_CONTROL_SHADER: TessellationControlShader,
            GL.GL_TESS_EVALUATION_SHADER: TessellationEvaluationShader,
            GL.GL_GEOMETRY_SHADER: GeometryShader,
            GL.GL_FRAGMENT_SHADER: FragmentShader,
        }[type](*args, **kwargs)
    @property
    def info_log(self):
        return GL.glGetShaderInfoLog(self._value)
    @property
    def compile_status(self):
        return GL.glGetShaderiv(self._value, GL.GL_COMPILE_STATUS)
    @utilities.universalmethod
    def source(cls, obj, source):
        GL.glShaderSource(obj._value, source)
    @utilities.universalmethod
    def compile(cls, obj):
        GL.glCompileShader(obj._value)


class ComputeShader(Shader):
    _type = GL.GL_COMPUTE_SHADER

class VertexShader(Shader):
    _type = GL.GL_VERTEX_SHADER

class TessellationControlShader(Shader):
    _type = GL.GL_TESS_CONTROL_SHADER

class TessellationEvaluationShader(Shader):
    _type = GL.GL_TESS_EVALUATION_SHADER

class GeometryShader(Shader):
    _type = GL.GL_GEOMETRY_SHADER

class FragmentShader(Shader):
    _type = GL.GL_FRAGMENT_SHADER


class Program(handles.Handle):
    @classmethod
    def _create(cls):
        return GL.glCreateProgram()
    @classmethod
    def _delete(cls, value):
        GL.glDeleteProgram(value)
    @property
    def info_log(self):
        return GL.glGetProgramInfoLog(self._value)
    @property
    def link_status(self):
        return GL.glGetProgramiv(self._value, GL.GL_LINK_STATUS)
    @utilities.universalmethod
    def attach(cls, obj, shader):
        GL.glAttachShader(obj._value, shader._value)
    @utilities.universalmethod
    def detach(cls, obj, shader):
        GL.glDetachShader(obj._value, shader._value)
    @utilities.universalmethod
    def link(cls, obj):
        GL.glLinkProgram(obj._value)
    @utilities.universalmethod
    def bind(cls, obj):
        GL.glUseProgram(obj._value)
    @utilities.universalmethod
    def unbind(cls, obj):
        GL.glUseProgram(obj._null)
