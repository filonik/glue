import contextlib as cl

import OpenGL
from OpenGL import GL

from encore import accessors

from .handles import scoped, bound, mapped
from .types import *


DEFAULT_CLEAR_MASK = GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT

def as_bool(value):
    return GL.GL_TRUE if value else GL.GL_FALSE

def clear_color(color):
    GL.glClearColor(
        accessors.getitem(color, 0, 1.0),
        accessors.getitem(color, 1, 1.0),
        accessors.getitem(color, 2, 1.0),
        accessors.getitem(color, 3, 1.0)
    )

def clear_depth(depth):
    GL.glClearDepth(depth)

def clear_stencil(stencil):
    GL.glClearStencil(stencil)

def clear(mask=DEFAULT_CLEAR_MASK):
    GL.glClear(mask)

def color_mask(value):
    GL.glColorMask(
        as_bool(accessors.getitem(value, 0, True)),
        as_bool(accessors.getitem(value, 1, True)),
        as_bool(accessors.getitem(value, 2, True)),
        as_bool(accessors.getitem(value, 3, True))
    )

def depth_mask(value):
    GL.glDepthMask(as_bool(value))

def stencil_mask(value):
    GL.glStencilMask(value)

def draw_buffer(buffer):
    GL.glDrawBuffer(buffer)

def enable(capability):
    GL.glEnable(capability)
    
def disable(capability):
    GL.glDisable(capability)

@cl.contextmanager
def enabled(capability):
    try:
        enable(capability)
        yield
    finally:
        disable(capability)

@cl.contextmanager
def disabled(capability):
    try:
        disable(capability)
        yield
    finally:
        enable(capability)

def flush():
    GL.glFlush()

def viewport(size, offset=(0, 0)):
    GL.glViewport(
        accessors.getitem(offset, 0, 0),
        accessors.getitem(offset, 1, 0),
        accessors.getitem(size, 0, 0),
        accessors.getitem(size, 1, 0)
    )
