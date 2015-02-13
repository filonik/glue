from __future__ import print_function

import ctypes

import OpenGL
from OpenGL import GL, arrays

# Functions that are not wrapped nicely in PyOpenGL yet.

def glGetProgramInterfaceiv(program, programInterface, pname):
    params = arrays.GLintArray.zeros((1,))
    GL.glGetProgramInterfaceiv(program, programInterface, pname, params)
    return params[0]

def glGetProgramResourceiv(program, programInterface, index, keys):
    length = ctypes.c_void_p(0) #arrays.GLintArray.zeros((1,)) # unused
    props = arrays.GLintArray.zeros((len(keys),))
    params = arrays.GLintArray.zeros((len(keys),))
    props[:] = keys
    GL.glGetProgramResourceiv(program, programInterface, index, len(props), props, len(params), length, params)
    return params
    
def glGetProgramResourceName(program, programInterface, index):
    length = ctypes.c_void_p(0) #arrays.GLintArray.zeros((1,)) # unused
    bufSize = glGetProgramResourceiv(program, programInterface, index, [GL.GL_NAME_LENGTH])[0] + 1
    name = ctypes.create_string_buffer(bufSize)
    GL.glGetProgramResourceName(program, programInterface, index, bufSize, length, name)
    return name.value
