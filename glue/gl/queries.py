from __future__ import absolute_import, division, print_function

import OpenGL
from OpenGL import GL, arrays

from . import resources

import logging
log = logging.getLogger(__name__)

class Query(resources.GLResource):
    @classmethod
    def create_handle(cls):
        arr = GL.glGenQueries(1)
        return arr[0]
    
    @classmethod
    def delete_handle(cls, handle):
        arr = arrays.GLuintArray.asArray([handle])
        size = arrays.GLuintArray.arraySize(arr)
        GL.glDeleteQueries(size, arr)
    
    @property
    def result(self):
        result = arrays.GLuintArray.zeros((1,))
        GL.glGetQueryObjectuiv(self._handle, GL.GL_QUERY_RESULT, result)
        return result