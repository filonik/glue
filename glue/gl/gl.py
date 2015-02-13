from __future__ import absolute_import, division, print_function

import ctypes
import importlib

import six

import OpenGL
from OpenGL import GL

from . import types, funcs

from ..decorators import indexedproperty
from ..flyweights import Resource
from ..utilities import nth, Unspecified, specified, getspecified

import logging
log = logging.getLogger(__name__)

DEFAULT_CLEAR_MASK = GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT

DEFAULT_BUFFER_USAGE = GL.GL_STATIC_DRAW

backend = None

def _set_backend(name):
    global backend
    backend = importlib.import_module('.' + name, 'glue.gl.backends')

def clear_color(color):
    GL.glClearColor(
        nth(color, 0, 0.0),
        nth(color, 1, 0.0),
        nth(color, 2, 0.0),
        nth(color, 3, 1.0)
    )

def clear(mask=DEFAULT_CLEAR_MASK):
    GL.glClear(mask)

def cleanup(context=Unspecified):
    if not specified(context):
        context = backend.Context.get_current()
    
    for cls in six.iterkeys(context._references):
        cls.cleanup(context=context)

class GLResource(Resource):
    _zero_handle = 0
    
    @classmethod
    def references(cls, context=Unspecified):
        if not specified(context):
            context = backend.Context.get_current()
        
        return context._references[cls]
        
class Shader(GLResource):
    _type = None
    
    @classmethod
    def create_handle(cls):
        return GL.glCreateShader(cls._type)
    
    @classmethod
    def delete_handle(cls, handle):
        GL.glDeleteShader(handle)
    
    @property
    def compile_status(self):
        return GL.glGetShaderiv(self._handle, GL.GL_COMPILE_STATUS)
    
    @property
    def info_log(self):
        return GL.glGetShaderInfoLog(self._handle)
    
    def set_source(self, source):
        GL.glShaderSource(self._handle, source)
    
    def compile(self):
        GL.glCompileShader(self._handle)
        
        if self.compile_status != 1:
            raise Exception("Shader Compile Error:\n%s" % (self.info_log,))

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

class Program(GLResource):
    @classmethod
    def bind(cls, obj):
        GL.glUseProgram(cls.handle(obj))
    
    @classmethod
    def create_handle(self):
        return GL.glCreateProgram()
    
    @classmethod
    def delete_handle(cls, handle):
        GL.glDeleteProgram(handle)
    
    @indexedproperty
    def uniforms(self, key): 
        return GL.glGetUniformLocation(self._handle, key)
    
    @uniforms.setter
    def uniforms(self, key, value):
        location = self.uniforms[key]
        if location != -1:
            type = types.gltype_tensor(value)
            setter = funcs.uniform_setter(type)
            setter(location, value)
        else:
            log.warn('Ignoring uniform "%s".' % (key,))
    
    @indexedproperty
    def attributes(self, key): 
        return GL.glGetAttribLocation(self._handle, key)
    
    @attributes.setter
    def attributes(self, key, value):
        location = self.attributes[key]
        if location != -1:
            type = value.type.dtype[key] if isinstance(value.type.dtype, dict) else value.type.dtype
            setter = funcs.attribute_setter(type)
            setter(location, value._handle)
        else:
            log.warn('Ignoring attribute "%s".' % (key,))
    
    @property
    def link_status(self):
        return GL.glGetProgramiv(self._handle, GL.GL_LINK_STATUS)
    
    @property
    def info_log(self):
        return GL.glGetProgramInfoLog(self._handle)
    
    def attach(self, shader):
        GL.glAttachShader(self._handle, shader._handle)
        
    def detach(self, shader):
        GL.glDetachShader(self._handle, shader._handle)
    
    def link(self):
        GL.glLinkProgram(self._handle)
    
        if self.link_status != 1:
            raise Exception("Program Link Error:\n%s" % (self.info_log,))

class VertexArray(GLResource):
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

class Buffer(GLResource):
    _target = None
    
    @classmethod
    def bind(cls, obj):
        GL.glBindBuffer(cls._target, cls.handle(obj))
    
    def __init__(self, *args, **kwargs):
        super(Buffer, self).__init__(*args, **kwargs)
        self._type = None
    
    @property
    def type(self):
        return self._type
    
    @classmethod
    def create_handle(self):
        return GL.glGenBuffers(1)
    
    @classmethod
    def delete_handle(cls, handle):
        GL.glDeleteBuffers(handle)
    
    def set_data(self, data, usage=DEFAULT_BUFFER_USAGE):
        type = types.gltype(data)
        GL.glBufferData(self._target, data.nbytes, data, usage)
        self._type = type
        
    def set_sub_data(self, data, offset=0):
        type = types.gltype(data)
        GL.glBufferSubData(self._target, offset, data.nbytes, data)

class ArrayBuffer(Buffer):
    _target = GL.GL_ARRAY_BUFFER

class ElementArrayBuffer(Buffer):
    _target = GL.GL_ELEMENT_ARRAY_BUFFER

VertexArrayObject = VertexArray
VertexBufferObject = ArrayBuffer
IndexBufferObject = ElementArrayBuffer

class Texture(GLResource):
    _target = None
    
    @classmethod
    def create_handle(cls):
        print('Create Texture.')
        return GL.glGenTextures(1)
    
    @classmethod
    def delete_handle(cls, handle):
        print('Delete Texture.')
        GL.glDeleteTextures(handle)
    

    