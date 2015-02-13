from __future__ import absolute_import, division, print_function

import functools as ft

def debug_mock_printer(result=None):
    def decorator(func):
        @ft.wraps(func)
        def decorated(*args, **kwargs):
            print('%s(%s)' % (func.__name__, ','.join(map(str, args))))
            return result
        return decorated
    return decorator

def mock(GL):
    GL.glEnableVertexAttribArray = debug_mock_printer()(GL.glEnableVertexAttribArray)
    GL.glDisableVertexAttribArray = debug_mock_printer()(GL.glDisableVertexAttribArray)
    
    GL.glBindBuffer = debug_mock_printer()(GL.glBindBuffer)
    GL.glBufferData = debug_mock_printer()(GL.glBufferData)
    GL.glBufferSubData = debug_mock_printer()(GL.glBufferSubData)
    
    GL.glVertexAttribPointer = debug_mock_printer()(GL.glVertexAttribPointer)
    GL.glVertexAttribIPointer = debug_mock_printer()(GL.glVertexAttribIPointer)
    GL.glVertexAttribLPointer = debug_mock_printer()(GL.glVertexAttribLPointer)
    
    GL.glUniform1fv = debug_mock_printer()(GL.glUniform1fv)
    GL.glUniform2fv = debug_mock_printer()(GL.glUniform2fv)
    GL.glUniform3fv = debug_mock_printer()(GL.glUniform3fv)
    GL.glUniform4fv = debug_mock_printer()(GL.glUniform4fv)
    
    GL.glUniformMatrix2fv = debug_mock_printer()(GL.glUniformMatrix2fv)
    GL.glUniformMatrix3fv = debug_mock_printer()(GL.glUniformMatrix3fv)
    GL.glUniformMatrix4fv = debug_mock_printer()(GL.glUniformMatrix4fv)
    GL.glUniformMatrix2x3fv = debug_mock_printer()(GL.glUniformMatrix2x3fv)
    GL.glUniformMatrix2x4fv = debug_mock_printer()(GL.glUniformMatrix2x4fv)
    GL.glUniformMatrix3x2fv = debug_mock_printer()(GL.glUniformMatrix3x2fv)
    GL.glUniformMatrix3x4fv = debug_mock_printer()(GL.glUniformMatrix3x4fv)
    GL.glUniformMatrix4x2fv = debug_mock_printer()(GL.glUniformMatrix4x2fv)
    GL.glUniformMatrix4x3fv = debug_mock_printer()(GL.glUniformMatrix4x3fv)
    
    GL.glUniform1iv = debug_mock_printer()(GL.glUniform1iv)
    GL.glUniform2iv = debug_mock_printer()(GL.glUniform2iv)
    GL.glUniform3iv = debug_mock_printer()(GL.glUniform3iv)
    GL.glUniform4iv = debug_mock_printer()(GL.glUniform4iv)
    
    GL.glUniform1uiv = debug_mock_printer()(GL.glUniform1uiv)
    GL.glUniform2uiv = debug_mock_printer()(GL.glUniform2uiv)
    GL.glUniform3uiv = debug_mock_printer()(GL.glUniform3uiv)
    GL.glUniform4uiv = debug_mock_printer()(GL.glUniform4uiv)
    
    return GL