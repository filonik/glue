from __future__ import absolute_import, division, print_function

import OpenGL
from OpenGL import GL, arrays

from . import resources

import logging
log = logging.getLogger(__name__)

class Query(resources.GLResource):
    @classmethod
    def create_handle(cls):
        return GL.glGenQueries(1)
    
    @classmethod
    def delete_handle(cls, handle):
        GL.glDeleteQueries(1, GL.GLuint(handle))
    
    @property
    def result(self)
        result = arrays.GLuintArray.zeros((1,))
        GL.glGetQueryObjectuiv(self._handle, GL_QUERY_RESULT, result)
        return result