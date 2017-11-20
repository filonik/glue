import OpenGL
from OpenGL import GL

from .. import utilities

from . import handles

DEFAULT_TEXTURE_FORMAT = GL.GL_RGBA
DEFAULT_TEXTURE_TYPE = GL.GL_UNSIGNED_BYTE

DEFAULT_TEXTURE_FILTER = GL.GL_LINEAR, GL.GL_LINEAR
DEFAULT_TEXTURE_WRAP = GL.GL_REPEAT, GL.GL_REPEAT, GL.GL_REPEAT

SIZED_FORMAT_TO_BASE_FORMAT = {
    GL.GL_RED: GL.GL_RED,
    GL.GL_RG: GL.GL_RG,
    GL.GL_RGB: GL.GL_RGB,
    GL.GL_RGBA: GL.GL_RGBA,
    GL.GL_R32F: GL.GL_RED,
    GL.GL_RG32F: GL.GL_RG,
    GL.GL_RGB32F: GL.GL_RGB, 
    GL.GL_RGBA32F: GL.GL_RGBA, 
    GL.GL_R32I: GL.GL_RED_INTEGER,
    GL.GL_RG32I: GL.GL_RG_INTEGER,
    GL.GL_RGB32I: GL.GL_RGB_INTEGER, 
    GL.GL_RGBA32I: GL.GL_RGBA_INTEGER, 
    GL.GL_R32UI: GL.GL_RED_INTEGER,
    GL.GL_RG32UI: GL.GL_RG_INTEGER,
    GL.GL_RGB32UI: GL.GL_RGB_INTEGER, 
    GL.GL_RGBA32UI: GL.GL_RGBA_INTEGER,
}

class Texture(handles.Handle):
    @classmethod
    def _create(cls):
        return GL.glGenTextures(1)
    @classmethod
    def _delete(cls, value):
        GL.glDeleteTextures(value)
    @classmethod
    def from_type(cls, type, *args, **kwargs):
        return {
            GL.GL_TEXTURE_1D: Texture1D,
            GL.GL_TEXTURE_2D: Texture2D,
            GL.GL_TEXTURE_3D: Texture3D,
        }[type](*args, **kwargs)
    @utilities.universalmethod
    def create(cls, obj):
        super().create(obj)
        
        with handles.bound(obj):
            filter, wrap = DEFAULT_TEXTURE_FILTER, DEFAULT_TEXTURE_WRAP
            
            GL.glTexParameterf(cls._type, GL.GL_TEXTURE_MIN_FILTER, filter[0])
            GL.glTexParameterf(cls._type, GL.GL_TEXTURE_MAG_FILTER, filter[1])
            
            GL.glTexParameterf(cls._type, GL.GL_TEXTURE_WRAP_S, wrap[0])
            GL.glTexParameterf(cls._type, GL.GL_TEXTURE_WRAP_T, wrap[1])
            GL.glTexParameterf(cls._type, GL.GL_TEXTURE_WRAP_R, wrap[2])
        
        return obj
    @utilities.universalmethod
    def bind(cls, obj):
        GL.glBindTexture(cls._type, obj._value)
    @utilities.universalmethod
    def unbind(cls, obj):
        GL.glBindTexture(cls._type, cls._null)


class Texture1D(Texture):
    _type = GL.GL_TEXTURE_1D

class Texture2D(Texture):
    _type = GL.GL_TEXTURE_2D

    @utilities.universalmethod
    def image(cls, obj, image, size, type=None, level=0, internalFormat=None, border=0, format=None):
        type = DEFAULT_TEXTURE_TYPE if type is None else type
        internalFormat = DEFAULT_TEXTURE_FORMAT if internalFormat is None else internalFormat
        format = internalFormat if format is None else format
        format = SIZED_FORMAT_TO_BASE_FORMAT.get(format, format)
        GL.glTexImage2D(cls._type, level, internalFormat, size[0], size[1], border, format, type, image)
    
    @utilities.universalmethod
    def sub_image(cls, obj, image, size, type=None, level=0, offset=(0,0), format=None):
        type = DEFAULT_TEXTURE_TYPE if type is None else type
        format = DEFAULT_TEXTURE_FORMAT if format is None else format
        format = SIZED_FORMAT_TO_BASE_FORMAT.get(format, format)
        GL.glTexSubImage2D(cls._type, level, offset[0], offset[1], size[0], size[1], format, type, image)


class Texture3D(Texture):
    _type = GL.GL_TEXTURE_3D