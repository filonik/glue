from __future__ import absolute_import, division, print_function

import OpenGL
from OpenGL import GL

from ..decorators import indexedproperty

from . import types, funcs, resources, textures

import logging
log = logging.getLogger(__name__)

class Shader(resources.GLResource):
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

class Program(resources.GLResource):
    @classmethod
    def bind(cls, obj):
        GL.glUseProgram(cls.handle(obj))
        if obj is not None:
            obj.texture_unit = 0
    
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
            if isinstance(value, textures.Texture):
                unit = self.texture_unit
                self.texture_unit += 1
                
                GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
                value.bind(value)
                value = GL.GLint(unit)
            
            type = types.gltype_tensor(value)
            setter = funcs.uniform_setter(type)
            setter(location, value)
        else:
            #log.warn('Ignoring uniform "%s".' % (key,))
            pass
    
    @indexedproperty
    def inputs(self, key): 
        return GL.glGetAttribLocation(self._handle, key)
    
    @inputs.setter
    def inputs(self, key, value):
        location = self.inputs[key]
        if location != -1:
            type = value.type.dtype[key] if isinstance(value.type.dtype, dict) else value.type
            setter = funcs.attribute_setter(type)
            setter(location, value._handle)
        else:
            #log.warn('Ignoring attribute "%s".' % (key,))
            pass
    
    @indexedproperty
    def outputs(self, key): 
        return GL.glGetFragDataLocation(self._handle, key)
    
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