from __future__ import absolute_import, division, print_function

import OpenGL
from OpenGL import GL

from . import resources

from ..utilities import Unspecified, specified, getspecified

DEFAULT_TEXTURE_FORMAT = GL.GL_RGBA
DEFAULT_TEXTURE_FORMATS = { 1: GL.GL_RED, 2: GL.GL_RG,  3: GL.GL_RGB, 4: GL.GL_RGBA, }
DEFAULT_TEXTURE_SIZE = (256, 256)
DEFAULT_TEXTURE_TYPE = GL.GL_UNSIGNED_BYTE

DEFAULT_TEXTURE_FILTER = GL.GL_LINEAR, GL.GL_LINEAR
DEFAULT_TEXTURE_WRAP = GL.GL_REPEAT, GL.GL_REPEAT, GL.GL_REPEAT

DEFAULT_SIZED_FORMAT_TO_BASE_FORMAT = {
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

TEXTURE_CUBEMAP_TARGETS = [
    GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X,
    GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
    GL.GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
    GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
    GL.GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
    GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_Z,
]

class Texture(resources.GLResource):
    _target = None
    
    @classmethod
    def fromtype(cls, type, *args, **kwargs):
        return {
            GL.GL_TEXTURE_1D: Texture1D,
            GL.GL_TEXTURE_2D: Texture2D,
            GL.GL_TEXTURE_3D: Texture3D,
            GL.GL_TEXTURE_CUBE_MAP: TextureCubeMap,
        }[type](*args, **kwargs)
    
    @classmethod
    def bind(cls, obj):
        GL.glBindTexture(cls._target, cls.handle(obj))
    
    @classmethod
    def create_handle(cls, *args, **kwargs):
        return GL.glGenTextures(1)
    
    @classmethod
    def delete_handle(cls, handle):
        GL.glDeleteTextures(handle)
        
    def __init__(self, filter=DEFAULT_TEXTURE_FILTER, wrap=DEFAULT_TEXTURE_WRAP, *args, **kwargs):
        super(Texture, self).__init__(*args, **kwargs)
        
        self.bind(self)
        
        GL.glTexParameterf(self._target, GL.GL_TEXTURE_MIN_FILTER, filter[0])
        GL.glTexParameterf(self._target, GL.GL_TEXTURE_MAG_FILTER, filter[1])
        
        GL.glTexParameterf(self._target, GL.GL_TEXTURE_WRAP_S, wrap[0])
        GL.glTexParameterf(self._target, GL.GL_TEXTURE_WRAP_T, wrap[1])
        GL.glTexParameterf(self._target, GL.GL_TEXTURE_WRAP_R, wrap[2])

class Texture1D(Texture):
    _target = GL.GL_TEXTURE_1D
    
    @classmethod
    def set_framebuffer(cls, attachment, obj):
        GL.glFramebufferTexture1D(GL.GL_FRAMEBUFFER, attachment, cls._target, cls.handle(obj), 0)
    
    #@classmethod
    def set_image(self, image, size, type=Unspecified, level=0, internalFormat=Unspecified, border=0, format=Unspecified):
        type = getspecified(type, DEFAULT_TEXTURE_TYPE)
        internalFormat = getspecified(internalFormat, DEFAULT_TEXTURE_FORMAT)
        format = getspecified(format, internalFormat)
        format = DEFAULT_SIZED_FORMAT_TO_BASE_FORMAT.get(format, format)
        GL.glTexImage1D(self._target, level, internalFormat, size[0], border, format, type, image)
    
    #@classmethod
    def set_sub_image(self, image, size, type=Unspecified, level=0, offset=(0,), format=Unspecified):
        type = getspecified(type, DEFAULT_TEXTURE_TYPE)
        format = getspecified(format, DEFAULT_TEXTURE_FORMAT)
        format = DEFAULT_SIZED_FORMAT_TO_BASE_FORMAT.get(format, format)
        GL.glTexSubImage1D(self._target, level, offset[0], size[0], format, type, image)

class Texture2D(Texture):
    _target = GL.GL_TEXTURE_2D
    
    @classmethod
    def set_framebuffer(cls, attachment, obj):
        GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, attachment, cls._target, cls.handle(obj), 0)
    
    #@classmethod
    def set_image(self, image, size, type=Unspecified, level=0, internalFormat=Unspecified, border=0, format=Unspecified):
        type = getspecified(type, DEFAULT_TEXTURE_TYPE)
        internalFormat = getspecified(internalFormat, DEFAULT_TEXTURE_FORMAT)
        format = getspecified(format, internalFormat)
        format = DEFAULT_SIZED_FORMAT_TO_BASE_FORMAT.get(format, format)
        GL.glTexImage2D(self._target, level, internalFormat, size[0], size[1], border, format, type, image)
    
    #@classmethod
    def set_sub_image(self, image, size, type=Unspecified, level=0, offset=(0,0), format=Unspecified):
        type = getspecified(type, DEFAULT_TEXTURE_TYPE)
        format = getspecified(format, DEFAULT_TEXTURE_FORMAT)
        format = DEFAULT_SIZED_FORMAT_TO_BASE_FORMAT.get(format, format)
        GL.glTexSubImage2D(self._target, level, offset[0], offset[1], size[0], size[1], format, type, image)

class Texture3D(Texture):
    _target = GL.GL_TEXTURE_3D
    
    @classmethod
    def set_framebuffer(cls, attachment, obj):
        GL.glFramebufferTexture3D(GL.GL_FRAMEBUFFER, attachment, cls._target, cls.handle(obj), 0)
    
    #@classmethod
    def set_image(self, image, size, type=Unspecified, level=0, internalFormat=Unspecified, border=0, format=Unspecified):
        type = getspecified(type, DEFAULT_TEXTURE_TYPE)
        internalFormat = getspecified(internalFormat, DEFAULT_TEXTURE_FORMAT)
        format = getspecified(format, internalFormat)
        format = DEFAULT_SIZED_FORMAT_TO_BASE_FORMAT.get(format, format)
        GL.glTexImage3D(self._target, level, internalFormat, size[0], size[1], size[2], border, format, type, image)
    
    #@classmethod
    def set_sub_image(self, image, size, type=Unspecified, level=0, offset=(0,0,0), format=Unspecified):
        type = getspecified(type, DEFAULT_TEXTURE_TYPE)
        format = getspecified(format, DEFAULT_TEXTURE_FORMAT)
        format = DEFAULT_SIZED_FORMAT_TO_BASE_FORMAT.get(format, format)
        GL.glTexSubImage3D(self._target, level, offset[0], offset[1], offset[2], size[0], size[1], size[2], format, type, image)

class TextureCubeMap(Texture):
    _target = GL.GL_TEXTURE_CUBE_MAP
    
    @classmethod
    def set_framebuffer(cls, attachment, obj):
        GL.glFramebufferTexture(GL.GL_FRAMEBUFFER, attachment, cls.handle(obj), 0)
    
    #@classmethod
    def set_image(self, image, size, type=Unspecified, level=0, internalFormat=Unspecified, border=0, format=Unspecified, target=Unspecified):
        type = getspecified(type, DEFAULT_TEXTURE_TYPE)
        internalFormat = getspecified(internalFormat, DEFAULT_TEXTURE_FORMAT)
        format = getspecified(format, internalFormat)
        format = DEFAULT_SIZED_FORMAT_TO_BASE_FORMAT.get(format, format)
        target = getspecified(target, self._target)
        GL.glTexImage2D(target, level, internalFormat, size[0], size[1], border, format, type, image)
    
    #@classmethod
    def set_sub_image(self, image, size, type=Unspecified, level=0, offset=(0,0), format=Unspecified, target=Unspecified):
        type = getspecified(type, DEFAULT_TEXTURE_TYPE)
        format = getspecified(format, DEFAULT_TEXTURE_FORMAT)
        format = DEFAULT_SIZED_FORMAT_TO_BASE_FORMAT.get(format, format)
        target = getspecified(target, self._target)
        GL.glTexSubImage2D(target, level, offset[0], offset[1], size[0], size[1], format, type, image)

