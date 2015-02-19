from __future__ import absolute_import, division, print_function

import OpenGL
from OpenGL import GL

from . import resources

DEFAULT_TEXTURE_FORMAT = GL.GL_RGBA
DEFAULT_TEXTURE_FILTER = GL.GL_LINEAR, GL.GL_LINEAR
DEFAULT_TEXTURE_WRAP = GL.GL_REPEAT, GL.GL_REPEAT, GL.GL_REPEAT

class Texture(resources.GLResource):
    _target = None
    
    @classmethod
    def bind(cls, obj):
        GL.glBindTexture(cls._target, cls.handle(obj))
    
    @classmethod
    def create_handle(cls):
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
        GL.glFramebufferTexture1D(GL.GL_FRAMEBUFFER, attachment, self._target, cls.handle(obj))
    
    def set_image(self, image, size, type, level=0, internalFormat=DEFAULT_TEXTURE_FORMAT, border=0, format=DEFAULT_TEXTURE_FORMAT):
        GL.glTexImage1D(self._target, level, internalFormat, size[0], border, format, type, image)
    
    def set_sub_image(self, image, size, type, offset=(0,), format=DEFAULT_TEXTURE_FORMAT):
        GL.glTexSubImage1D(self._target, level, offset[0], size[0], format, type, image)

class Texture2D(Texture):
    _target = GL.GL_TEXTURE_2D
    
    @classmethod
    def set_framebuffer(cls, attachment, obj):
        GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, attachment, self._target, cls.handle(obj))
    
    def set_image(self, image, size, type, level=0, internalFormat=DEFAULT_TEXTURE_FORMAT, border=0, format=DEFAULT_TEXTURE_FORMAT):
        GL.glTexImage2D(self._target, level, internalFormat, size[0], size[1], border, format, type, image)
    
    def set_sub_image(self, image, size, type, offset=(0,0), format=DEFAULT_TEXTURE_FORMAT):
        GL.glTexSubImage2D(self._target, level, offset[0], offset[1], size[0], size[1], format, type, image)

class Texture3D(Texture):
    _target = GL.GL_TEXTURE_3D
    
    @classmethod
    def set_framebuffer(cls, attachment, obj):
        GL.glFramebufferTexture3D(GL.GL_FRAMEBUFFER, attachment, self._target, cls.handle(obj))
    
    def set_image(self, image, size, type, level=0, internalFormat=DEFAULT_TEXTURE_FORMAT, border=0, format=DEFAULT_TEXTURE_FORMAT):
        GL.glTexImage3D(self._target, level, internalFormat, size[0], size[1], size[2], border, format, type, image)
    
    def set_sub_image(self, image, size, type, offset=(0,0,0), format=DEFAULT_TEXTURE_FORMAT):
        GL.glTexSubImage3D(self._target, level, offset[0], offset[1], offset[2], size[0], size[1], size[2], format, type, image)
