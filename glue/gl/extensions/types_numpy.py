from __future__ import absolute_import, division, print_function

import functools as ft

import OpenGL
from OpenGL import GL

import numpy as np

from ...utilities import reversedict

_gltypes_to_nptypes = {
    GL.GL_BOOL: np.bool,
    GL.GL_UNSIGNED_BYTE: np.uint8,
    GL.GL_BYTE: np.int8,
    GL.GL_UNSIGNED_SHORT: np.uint16,
    GL.GL_SHORT: np.int16,
    GL.GL_UNSIGNED_INT: np.uint32,
    GL.GL_INT: np.int32,
    GL.GL_HALF_FLOAT: np.float16,
    GL.GL_FLOAT: np.float32,
    GL.GL_DOUBLE: np.float64,
}

_nptypes_to_gltypes = reversedict(_gltypes_to_nptypes)

def _gltype_tensor_extension(func):
    from ..types import GLTensorType
    @ft.wraps(func)
    def gltype_tensor(obj):
        for nptype, gltype in _nptypes_to_gltypes.items():
            if isinstance(obj, nptype):
                return GLTensorType(gltype, ())
        
        if isinstance(obj, np.ndarray):
            if len(obj.shape) < 3 and np.all(np.array(obj.shape) < 5) and obj.dtype.type in _nptypes_to_gltypes:
                _type = _nptypes_to_gltypes[obj.dtype.type]
                return GLTensorType(_type, obj.shape)
        
        return func(obj)
    return gltype_tensor

def _gltype_array_extension(func):
    from ..types import GLArrayType
    from ..types import gltype
    @ft.wraps(func)
    def gltype_array(obj, offset=0):
        if isinstance(obj, np.ndarray):
            size, stride = obj.shape[0], obj.strides[0]
            if obj.dtype.names is None:
                type, sizes, dtype = _nptypes_to_gltypes[obj.dtype.type], obj.shape[1:], gltype(obj[0])
                return GLArrayType(size, stride, offset, dtype)
            else:
                offsets = np.r_[0, [obj.dtype[name].itemsize for name in obj.dtype.names]].cumsum()
                dtype = {name: gltype_array(obj[name], offset=offset) for name, offset in zip(obj.dtype.names, offsets)}
                return GLArrayType(size, stride, offset, dtype)
        
        return func(obj)
    return gltype_array