from __future__ import absolute_import, division, print_function

import collections

from ..flyweights import Resource

class Context(Resource):
    __references = dict()
    
    @classmethod
    def references(cls, context=Unspecified):
        return cls.__references
    
    @classmethod
    def create_handle(cls, window):
        pass
    
    @classmethod
    def delete_handle(cls, handle):
        pass

    def __init__(self, *args, **kwargs):
        super(Context, self).__init__(*args, **kwargs)
        
        self._references = collections.defaultdict(dict)
    
    def dispose(self):
        for cls in self._references:
            references = self._references[cls]
            for handle, reference in list(six.iteritems(references)):
                del references[handle]
                cls.delete(handle)
        
        super(Context, self).dispose()