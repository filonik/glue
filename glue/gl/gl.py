from __future__ import absolute_import, division, print_function

import ctypes
import importlib

import six

import OpenGL
from OpenGL import GL

#from ._debug import mock
#GL = mock(GL)

from . import types, funcs, utilities

from ..decorators import classproperty
from ..utilities import nth, Unspecified, specified, getspecified

import logging
log = logging.getLogger(__name__)

DEFAULT_CLEAR_MASK = GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT

backend = None

def _get_backend():
    global backend
    return backend

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

def clear_depth(depth):
    GL.glClearDepth(depth)

def clear(mask=DEFAULT_CLEAR_MASK):
    GL.glClear(mask)

def cleanup(context=Unspecified):
    if not specified(context):
        context = backend.Context.get_current()
    
    for cls in six.iterkeys(context._references):
        cls.cleanup(context=context)

from .buffers import *
from .shaders import *
from .textures import *

class Framebuffer(resources.GLResource):
    @classmethod
    def create_handle(cls):
        return GL.glGenFramebuffers(1)
    
    @classmethod
    def delete_handle(cls, handle):
        GL.glDeleteFramebuffers(1, GL.GLuint(handle))
    
    @classmethod
    def bind(cls, obj):
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, cls.handle(obj))
    
    @classproperty
    def status(self):
        return GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER)
    
    def attach(self, attachment_point, attachment):
        attachment.set_framebuffer(attachment_point, attachment)
    
    def detach(self, attachment_point, attachment):
        attachment.set_framebuffer(attachment_point, None)
    
class Renderbuffer(resources.GLResource):
    @classmethod
    def create_handle(cls):
        return GL.glGenRenderbuffers(1)
    
    @classmethod
    def delete_handle(cls, handle):
        GL.glDeleteRenderbuffers(1, GL.GLuint(handle))
    
    @classmethod
    def bind(cls, obj):
        GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, cls.handle(obj))
    
    @classmethod
    def set_framebuffer(cls, attachment, obj):
        GL.glFramebufferRenderbuffer(GL.GL_FRAMEBUFFER, attachment, GL.GL_RENDERBUFFER, cls.handle(obj))
    
    @classmethod
    def set_storage(cls, storage, size):
        GL.glRenderbufferStorage(GL.GL_RENDERBUFFER, storage, size[0], size[1])
    
from .extensions import buffers_numpy
from .extensions import textures_numpy
from .extensions import textures_pil
