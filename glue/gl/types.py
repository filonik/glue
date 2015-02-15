from __future__ import absolute_import, division, print_function

import collections
import functools as ft

import OpenGL
from OpenGL import GL

from ..utilities import reversedict

#from ._debug import mock
#GL = mock(GL)

_gltype_suffixes = {
    GL.GL_BOOL: 'b',
    GL.GL_UNSIGNED_BYTE: 'ui8',
    GL.GL_BYTE: 'i8',
    GL.GL_UNSIGNED_SHORT: 'ui16',
    GL.GL_SHORT: 'i16',
    GL.GL_UNSIGNED_INT: 'ui',
    GL.GL_INT: 'i',
    GL.GL_FLOAT: 'f',
    GL.GL_DOUBLE: 'd',
}

from ._types_gl import _gltype_sizeof, _gltype_stridesof

def _glcommontype(obj):
    return (obj.type, obj.sizes)

def _gltype_lt(a, b):
    return _glcommontype(a) < _glcommontype(b)

def _gltype_eq(a, b):
    return _glcommontype(a) == _glcommontype(b)

@ft.total_ordering
class GLTensorType(collections.namedtuple('GLTensorType', ['type', 'sizes'])):
    @property
    def rank(self):
        return len(self.sizes)
    
    @property
    def strides(self):
        return _gltype_stridesof(self.type, self.sizes)
    
    __lt__ = _gltype_lt
    __eq__ = _gltype_eq
    
    def __repr__(self):
        names = ['scalar', 'vector', 'matrix']
        return names[self.rank] + 'x'.join(map(str, self.sizes)) + _gltype_suffixes[self.type]

@ft.total_ordering
class GLArrayType(collections.namedtuple('GLArrayType', ['size', 'stride', 'offset', 'dtype'])):
    @property
    def type(self):
        if isinstance(self.dtype, dict):
            return {name: self.dtype[name].type for name in self.dtype}
        return self.dtype.type
    
    @property
    def sizes(self):
        if isinstance(self.dtype, dict):
            return {name: self.dtype[name].sizes for name in self.dtype}
        return (self.size,) + self.dtype.sizes
    
    @property
    def rank(self):
        if isinstance(self.dtype, dict):
            return {name: self.dtype[name].rank for name in self.dtype}
        return 1 + self.dtype.rank
    
    @property
    def strides(self):
        if isinstance(self.dtype, dict):
            return {name: self.dtype[name].strides for name in self.dtype}
        return (self.stride,) + self.dtype.strides
    
    __lt__ = _gltype_lt
    __eq__ = _gltype_eq
    
    def __repr__(self):
        return 'array<%s, %s>' % (self.size, repr(self.dtype))

GLTypes = (GLTensorType, GLArrayType)

def gltype_tensor(obj):
    raise TypeError('Failed to deduce GLTensorType from object of type "%s".' % (type(obj).__name__,))

def gltype_array(obj):
    raise TypeError('Failed to deduce GLArrayType from object of type "%s".' % (type(obj).__name__,))

def gltype(obj):
    if isinstance(obj, GLTypes):
        return obj
    
    try:
        return gltype_tensor(obj)
    except TypeError:
        try:
            return gltype_array(obj)
        except TypeError:
            raise TypeError('Failed to deduce GLType from object of type "%s".' % (type(obj).__name__,))

def _generate_gltensortypes(type, rank, start=2, stop=5):
    if rank == 0:
        yield GLTensorType(type, ())
    else:
        for size in range(start, stop):
            for t in _generate_gl_tensor_types(type, rank-1, start, stop):
                yield GLTensorType(type, (size,) + t.sizes)

# Extensions

from ._types_gl import _gltype_tensor_extension, _gltype_array_extension

gltype_tensor = _gltype_tensor_extension(gltype_tensor)
gltype_array = _gltype_array_extension(gltype_array)

from ._types_glsl import _gltype_tensor_extension, _gltype_array_extension

gltype_tensor = _gltype_tensor_extension(gltype_tensor)
gltype_array = _gltype_array_extension(gltype_array)

from .extensions.types_numpy import _gltype_tensor_extension, _gltype_array_extension

gltype_tensor = _gltype_tensor_extension(gltype_tensor)
gltype_array = _gltype_array_extension(gltype_array)

# Types

bvec2_t = gltype(GL.GL_BOOL_VEC2)
bvec3_t = gltype(GL.GL_BOOL_VEC3)
bvec4_t = gltype(GL.GL_BOOL_VEC4)

ivec2_t = gltype(GL.GL_INT_VEC2)
ivec3_t = gltype(GL.GL_INT_VEC3)
ivec4_t = gltype(GL.GL_INT_VEC4)

vec2_t = gltype(GL.GL_FLOAT_VEC2)
vec3_t = gltype(GL.GL_FLOAT_VEC3)
vec4_t = gltype(GL.GL_FLOAT_VEC4)
mat2_t = gltype(GL.GL_FLOAT_MAT2)
mat3_t = gltype(GL.GL_FLOAT_MAT3)
mat4_t = gltype(GL.GL_FLOAT_MAT4)
mat2x3_t = gltype(GL.GL_FLOAT_MAT2x3)
mat2x4_t = gltype(GL.GL_FLOAT_MAT3x4)
mat3x2_t = gltype(GL.GL_FLOAT_MAT3x2)
mat3x4_t = gltype(GL.GL_FLOAT_MAT3x4)
mat4x2_t = gltype(GL.GL_FLOAT_MAT4x2)
mat4x3_t = gltype(GL.GL_FLOAT_MAT4x3)

dvec2_t = gltype(GL.GL_DOUBLE_VEC2)
dvec3_t = gltype(GL.GL_DOUBLE_VEC3)
dvec4_t = gltype(GL.GL_DOUBLE_VEC4)
dmat2_t = gltype(GL.GL_DOUBLE_MAT2)
dmat3_t = gltype(GL.GL_DOUBLE_MAT3)
dmat4_t = gltype(GL.GL_DOUBLE_MAT4)
dmat2x3_t = gltype(GL.GL_DOUBLE_MAT2x3)
dmat2x4_t = gltype(GL.GL_DOUBLE_MAT3x4)
dmat3x2_t = gltype(GL.GL_DOUBLE_MAT3x2)
dmat3x4_t = gltype(GL.GL_DOUBLE_MAT3x4)
dmat4x2_t = gltype(GL.GL_DOUBLE_MAT4x2)
dmat4x3_t = gltype(GL.GL_DOUBLE_MAT4x3)

def array_t(dtype, size=0, offset=0):
    return GLArrayType(size, dtype.strides[0], offset, dtype)