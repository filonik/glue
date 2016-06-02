from __future__ import print_function

import ctypes

import OpenGL
from OpenGL import GL, arrays

# Functions that are not wrapped nicely in PyOpenGL yet.

def getCompatibleSubroutines(program, shader_type, uniform_subroutine):
    count = GL.glGetActiveSubroutineUniformiv(program, shader_type, uniform_subroutine, GL.GL_NUM_COMPATIBLE_SUBROUTINES)
    buffer = arrays.GLintArray.zeros((count,))
    GL.glGetActiveSubroutineUniformiv(program, shader_type, uniform_subroutine, GL.GL_COMPATIBLE_SUBROUTINES, buffer)
    return buffer

def glGetActiveSubroutineName(program, shader_type, index):
    bufsize = 1024
    buffer = ctypes.create_string_buffer(bufsize)
    c_text = ctypes.cast(ctypes.pointer(ctypes.pointer(buffer)), ctypes.POINTER(ctypes.POINTER(GL.GLchar)))
    length = arrays.GLintArray.zeros((1,))
    GL.glGetActiveSubroutineName(program, shader_type, index, bufsize, length, buffer)
    return buffer.raw[:length]

def glGetActiveSubroutineUniformName(program, shader_type, index):
    bufsize = 1024
    buffer = ctypes.create_string_buffer(bufsize)
    c_text = ctypes.cast(ctypes.pointer(ctypes.pointer(buffer)), ctypes.POINTER(ctypes.POINTER(GL.GLchar)))
    length = arrays.GLintArray.zeros((1,))
    GL.glGetActiveSubroutineUniformName(program, shader_type, index, bufsize, length, buffer)
    return buffer.raw[:length]

def glGetProgramInterfaceiv(program, programInterface, pname):
    params = arrays.GLintArray.zeros((1,))
    GL.glGetProgramInterfaceiv(program, programInterface, pname, params)
    return params[0]

def glGetProgramResourceiv(program, programInterface, index, keys):
    length = arrays.GLintArray.zeros((1,)) # ctypes.c_void_p(0)
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

def glTransformFeedbackVaryings(program, varyings, buffer_mode):
    #TODO: Handle multiple strings...
    buffer = ctypes.create_string_buffer(varyings[0])
    c_text = ctypes.cast(ctypes.pointer(ctypes.pointer(buffer)), ctypes.POINTER(ctypes.POINTER(GL.GLchar)))
    GL.glTransformFeedbackVaryings(program, 1, c_text, buffer_mode)
