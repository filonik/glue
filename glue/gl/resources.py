from __future__ import absolute_import, division, print_function

from ..flyweights import Resource
from ..utilities import Unspecified, specified, getspecified

class GLResource(Resource):
    _zero_handle = 0
    
    @classmethod
    def references(cls, context=Unspecified):
        from . import gl
        
        if not specified(context):
            context = gl.backend.Context.get_current()
        
        return context._references[cls]