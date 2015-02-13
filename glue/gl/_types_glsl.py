from __future__ import absolute_import, division, print_function

import functools as ft

import OpenGL
from OpenGL import GL

from ..utilities import reversedict

_glsltensortypes_to_gltensortypes = {
    GL.GL_BOOL: (GL.GL_BOOL, ()),
    GL.GL_BOOL_VEC2: (GL.GL_BOOL, (2,)),
    GL.GL_BOOL_VEC3: (GL.GL_BOOL, (3,)),
    GL.GL_BOOL_VEC4: (GL.GL_BOOL, (4,)),
    
    GL.GL_UNSIGNED_INT: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_UNSIGNED_INT_VEC2: (GL.GL_UNSIGNED_INT, (2,)),
    GL.GL_UNSIGNED_INT_VEC3: (GL.GL_UNSIGNED_INT, (3,)),
    GL.GL_UNSIGNED_INT_VEC4: (GL.GL_UNSIGNED_INT, (4,)),
    
    GL.GL_INT: (GL.GL_INT, ()),
    GL.GL_INT_VEC2: (GL.GL_INT, (2,)),
    GL.GL_INT_VEC3: (GL.GL_INT, (3,)),
    GL.GL_INT_VEC4: (GL.GL_INT, (4,)),
    
    GL.GL_FLOAT: (GL.GL_FLOAT, ()),
    GL.GL_FLOAT_VEC2: (GL.GL_FLOAT, (2,)),
    GL.GL_FLOAT_VEC3: (GL.GL_FLOAT, (3,)),
    GL.GL_FLOAT_VEC4: (GL.GL_FLOAT, (4,)),
    GL.GL_FLOAT_MAT2: (GL.GL_FLOAT, (2, 2)),
    GL.GL_FLOAT_MAT3: (GL.GL_FLOAT, (3, 3)),
    GL.GL_FLOAT_MAT4: (GL.GL_FLOAT, (4, 4)),
    GL.GL_FLOAT_MAT2x3: (GL.GL_FLOAT, (2, 3)),
    GL.GL_FLOAT_MAT2x4: (GL.GL_FLOAT, (2, 4)),
    GL.GL_FLOAT_MAT3x2: (GL.GL_FLOAT, (3, 2)),
    GL.GL_FLOAT_MAT3x4: (GL.GL_FLOAT, (3, 4)),
    GL.GL_FLOAT_MAT4x2: (GL.GL_FLOAT, (4, 2)),
    GL.GL_FLOAT_MAT4x3: (GL.GL_FLOAT, (4, 3)),
    
    GL.GL_DOUBLE: (GL.GL_DOUBLE, ()),
    GL.GL_DOUBLE_VEC2: (GL.GL_DOUBLE, (2,)),
    GL.GL_DOUBLE_VEC3: (GL.GL_DOUBLE, (3,)),
    GL.GL_DOUBLE_VEC4: (GL.GL_DOUBLE, (4,)),
    GL.GL_DOUBLE_MAT2: (GL.GL_DOUBLE, (2, 2)),
    GL.GL_DOUBLE_MAT3: (GL.GL_DOUBLE, (3, 3)),
    GL.GL_DOUBLE_MAT4: (GL.GL_DOUBLE, (4, 4)),
    GL.GL_DOUBLE_MAT2x3: (GL.GL_DOUBLE, (2, 3)),
    GL.GL_DOUBLE_MAT2x4: (GL.GL_DOUBLE, (2, 4)),
    GL.GL_DOUBLE_MAT3x2: (GL.GL_DOUBLE, (3, 2)),
    GL.GL_DOUBLE_MAT3x4: (GL.GL_DOUBLE, (3, 4)),
    GL.GL_DOUBLE_MAT4x2: (GL.GL_DOUBLE, (4, 2)),
    GL.GL_DOUBLE_MAT4x3: (GL.GL_DOUBLE, (4, 3)),
}

_gltensortypes_to_glsltensortypes = reversedict(_glsltensortypes_to_gltensortypes)

_glslsamplertypes_to_gltensortypes = {
    GL.GL_SAMPLER_1D: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_SAMPLER_2D: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_SAMPLER_3D: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_SAMPLER_CUBE: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_SAMPLER_1D_SHADOW: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_SAMPLER_2D_SHADOW: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_SAMPLER_1D_ARRAY: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_SAMPLER_2D_ARRAY: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_SAMPLER_1D_ARRAY_SHADOW: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_SAMPLER_2D_ARRAY_SHADOW: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_SAMPLER_2D_MULTISAMPLE: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_SAMPLER_2D_MULTISAMPLE_ARRAY: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_SAMPLER_CUBE_SHADOW: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_SAMPLER_BUFFER: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_SAMPLER_2D_RECT: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_SAMPLER_2D_RECT_SHADOW: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_INT_SAMPLER_1D: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_INT_SAMPLER_2D: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_INT_SAMPLER_3D: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_INT_SAMPLER_CUBE: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_INT_SAMPLER_1D_ARRAY: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_INT_SAMPLER_2D_ARRAY: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_INT_SAMPLER_2D_MULTISAMPLE: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_INT_SAMPLER_BUFFER: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_INT_SAMPLER_2D_RECT: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_UNSIGNED_INT_SAMPLER_1D: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_UNSIGNED_INT_SAMPLER_2D: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_UNSIGNED_INT_SAMPLER_3D: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_UNSIGNED_INT_SAMPLER_CUBE: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_UNSIGNED_INT_SAMPLER_1D_ARRAY: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_UNSIGNED_INT_SAMPLER_2D_ARRAY: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_UNSIGNED_INT_SAMPLER_BUFFER: (GL.GL_UNSIGNED_INT, ()),
    GL.GL_UNSIGNED_INT_SAMPLER_2D_RECT: (GL.GL_UNSIGNED_INT, ()),
}

_glsltypes_to_gltensortypes = {}
_glsltypes_to_gltensortypes.update(_glsltensortypes_to_gltensortypes)
_glsltypes_to_gltensortypes.update(_glslsamplertypes_to_gltensortypes)

def hashable(obj):
    try:
        hash(obj)
    except TypeError:
        return False
    return True

def _gltype_tensor_extension(func):
    from .types import GLTensorType
    @ft.wraps(func)
    def gltype_tensor(obj):
        if hashable(obj) and obj in _glsltypes_to_gltensortypes:
            return GLTensorType(*_glsltypes_to_gltensortypes[obj])
        
        return func(obj)
    return gltype_tensor

def _gltype_array_extension(func):
    from .types import GLArrayType
    return func