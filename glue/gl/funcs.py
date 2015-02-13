from __future__ import absolute_import, division, print_function

import ctypes

import OpenGL
from OpenGL import GL

from .types import GLTypes, GLTensorType, GLArrayType, _glcommontype

_gl_lpointer_types = (GL.GL_DOUBLE,)
_gl_ipointer_types = (GL.GL_BYTE, GL.GL_UNSIGNED_BYTE, GL.GL_SHORT, GL.GL_UNSIGNED_SHORT, GL.GL_INT, GL.GL_UNSIGNED_INT,)
_gl_pointer_types = (GL.GL_HALF_FLOAT, GL.GL_FLOAT, GL.GL_DOUBLE, GL.GL_FIXED, GL.GL_INT_2_10_10_10_REV, GL.GL_UNSIGNED_INT_2_10_10_10_REV, GL.GL_UNSIGNED_INT_10F_11F_11F_REV,)

def _gltensortype_to_vertexattribpointer_func(gltensortype):
    if gltensortype.type in _gl_lpointer_types:
        return GL.glVertexAttribLPointer
    if gltensortype.type in _gl_ipointer_types:
        return GL.glVertexAttribIPointer
    if gltensortype.type in _gl_pointer_types:
        return GL.glVertexAttribPointer

_gltensortype_to_uniform_funcs = {
    (GL.GL_INT, ()): GL.glUniform1iv,
    (GL.GL_INT, (2,)): GL.glUniform2iv,
    (GL.GL_INT, (3,)): GL.glUniform3iv,
    (GL.GL_INT, (4,)): GL.glUniform4iv,
    (GL.GL_UNSIGNED_INT, ()): GL.glUniform1uiv,
    (GL.GL_UNSIGNED_INT, (2,)): GL.glUniform2uiv,
    (GL.GL_UNSIGNED_INT, (3,)): GL.glUniform3uiv,
    (GL.GL_UNSIGNED_INT, (4,)): GL.glUniform4uiv,
    (GL.GL_FLOAT, ()): GL.glUniform1fv,
    (GL.GL_FLOAT, (2,)): GL.glUniform2fv,
    (GL.GL_FLOAT, (3,)): GL.glUniform3fv,
    (GL.GL_FLOAT, (4,)): GL.glUniform4fv,
    (GL.GL_FLOAT, (2, 2)): GL.glUniformMatrix2fv,
    (GL.GL_FLOAT, (3, 3)): GL.glUniformMatrix2fv,
    (GL.GL_FLOAT, (4, 4)): GL.glUniformMatrix4fv,
    (GL.GL_FLOAT, (2, 3)): GL.glUniformMatrix2x3fv,
    (GL.GL_FLOAT, (2, 4)): GL.glUniformMatrix2x4fv,
    (GL.GL_FLOAT, (3, 2)): GL.glUniformMatrix3x2fv,
    (GL.GL_FLOAT, (3, 4)): GL.glUniformMatrix3x4fv,
    (GL.GL_FLOAT, (4, 2)): GL.glUniformMatrix4x2fv,
    (GL.GL_FLOAT, (4, 3)): GL.glUniformMatrix4x3fv,
}

def _gltensortype_to_uniform_func(gltype):
    return _gltensortype_to_uniform_funcs[_glcommontype(gltype)]

def uniform_setter(gltype):
    if not isinstance(gltype, GLTypes):
        raise TypeError('Argument should be tensor or array.')
    
    if isinstance(gltype, GLTensorType):
        func = _gltensortype_to_uniform_func(gltype)
        rank = len(gltype.sizes)
        count = 1
    if isinstance(gltype, GLArrayType):
        func = _gltensortype_to_uniform_func(gltype.dtype)
        rank = len(gltype.dtype.sizes)
        count = gltype.size
        
    if rank == 0:
        def uniform_scalar(location, value, type=None):
            assert (type is None) or (gltype == type), 'Cannot set uniform of "%s" with incompatible "%s".' % (gltype, type)
            func(location, count, value)
        return uniform_scalar
    elif rank == 1:
        def uniform_vector(location, value, type=None):
            assert (type is None) or (gltype == type), 'Cannot set uniform of "%s" with incompatible "%s".' % (gltype, type)
            func(location, count, value)
        return uniform_vector
    elif rank == 2:
        def uniform_matrix(location, value, type=None, transpose=False):
            assert (type is None) or (gltype == type), 'Cannot set uniform of "%s" with incompatible "%s".' % (gltype, type)
            func(location, count, transpose, value)
        return uniform_matrix

def vertex_attribute_pointer_setter(gltype):
    func = _gltensortype_to_vertexattribpointer_func(gltype.dtype)
    rank = len(gltype.dtype.sizes)
    if rank == 0:
        size = 1
        def vertex_attrib_pointer_scalar(location, normalized=False, stride=gltype.stride, offset=gltype.offset):
            func(location, size, gltype.type, normalized, stride, ctypes.c_void_p(offset))
        return vertex_attrib_pointer_scalar
    elif rank == 1:
        size = gltype.dtype.sizes[0]
        def vertex_attrib_pointer_vector(location, normalized=False, stride=gltype.stride, offset=gltype.offset):
            func(location, size, gltype.type, normalized, stride, ctypes.c_void_p(offset))
        return vertex_attrib_pointer_vector
    elif rank == 2:
        outer_size, size, inner_stride = gltype.dtype.sizes[0], gltype.dtype.sizes[1], gltype.dtype.strides[1]
        def vertex_attrib_pointer_matrix(location, normalized=False, stride=gltype.stride, offset=gltype.offset):
            for n in range(outer_size):
                func(location + n, size, gltype.type, normalized, stride, ctypes.c_void_p(offset + inner_stride * n))
        return vertex_attrib_pointer_matrix

def attribute_setter(gltype):
    if not isinstance(gltype, GLArrayType):
        raise TypeError('Argument should be array.')
    
    func = vertex_attribute_pointer_setter(gltype)
    def attribute(location, value, type=None, normalized=False):
        assert (type is None) or (gltype.dtype == type.dtype), 'Cannot set attribute of "%s" with incompatible "%s".' % (gltype.dtype, type.dtype)
        type = gltype if type is None else type
        if value is None:
            GL.glDisableVertexAttribArray(location)
        else:
            GL.glEnableVertexAttribArray(location)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, value)
            func(location, normalized=normalized, stride=type.stride, offset=type.offset)
    return attribute