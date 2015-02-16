from __future__ import absolute_import, division, print_function

import ctypes
import functools as ft

import OpenGL
from OpenGL import GL

from ..utilities import reversedict

# TODO: Add these?
#GL.GL_INT_2_10_10_10_REV, GL.GL_UNSIGNED_INT_2_10_10_10_REV
#GL.GL_UNSIGNED_INT_10F_11F_11F_REV
'''
GL.GL_UNSIGNED_BYTE_3_3_2,         GL.GLubyte,  3
GL.GL_UNSIGNED_BYTE_2_3_3_REV,     GL.GLubyte,  3
GL.GL_UNSIGNED_SHORT_5_6_5,        GL.GLushort, 3  
GL.GL_UNSIGNED_SHORT_5_6_5_REV,    GL.GLushort, 3           
GL.GL_UNSIGNED_SHORT_4_4_4_4,      GL.GLushort, 4
GL.GL_UNSIGNED_SHORT_4_4_4_4_REV,  GL.GLushort, 4       
GL.GL_UNSIGNED_SHORT_5_5_5_1,      GL.GLushort, 4
GL.GL_UNSIGNED_SHORT_1_5_5_5_REV,  GL.GLushort, 4       
GL.GL_UNSIGNED_INT_8_8_8_8,        GL.GLuint,   4
GL.GL_UNSIGNED_INT_8_8_8_8_REV,    GL.GLuint,   4
GL.GL_UNSIGNED_INT_10_10_10_2,     GL.GLuint,   4
GL.GL_UNSIGNED_INT_2_10_10_10_REV, GL.GLuint,   4
'''

_gltypes_to_ctypes = {
    GL.GL_BOOL: GL.GLboolean,
    GL.GL_UNSIGNED_BYTE: GL.GLubyte,
    GL.GL_BYTE: GL.GLbyte,
    GL.GL_UNSIGNED_SHORT: GL.GLushort,
    GL.GL_SHORT: GL.GLshort,
    GL.GL_UNSIGNED_INT: GL.GLuint,
    GL.GL_INT: GL.GLint,
    GL.GL_FLOAT: GL.GLfloat,
    GL.GL_DOUBLE: GL.GLdouble,
}

_ctypes_to_gltypes = reversedict(_gltypes_to_ctypes)

def _gltype_sizeof(gltype):
    return ctypes.sizeof(_gltypes_to_ctypes[gltype])

def _gltype_stridesof(gltype, sizes):
    if len(sizes) == 0:
        return ()
    elif len(sizes) == 1:
        return (_gltype_sizeof(gltype),)
    else:
        head, tail = sizes[1], sizes[1:]
        strides = _gltype_stridesof(gltype, tail)
        stride = head * strides[0]
        return (stride,) + strides

def _gltype_tensor_extension(func):
    from .types import GLTensorType
    @ft.wraps(func)
    def gltype_tensor(obj):
        for ctype, gltype in _ctypes_to_gltypes.items():
            if isinstance(obj, ctype):
                return GLTensorType(gltype, ())
        
        return func(obj)
    return gltype_tensor

def _gltype_array_extension(func):
    from .types import GLArrayType
    return func