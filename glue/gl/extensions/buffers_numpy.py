from __future__ import absolute_import, division, print_function

import functools as ft

import numpy as np

from ...decorators import decorationmethod

from ..buffers import *

@decorationmethod(Buffer)
def set_data(func):
    @ft.wraps(func)
    def decorated(obj, data, *args, **kwargs):
        if isinstance(data, np.ndarray):
            size = data.nbytes
            return func(obj, data, size, *args, **kwargs)
        
        return func(obj, data, *args, **kwargs)
    
    return decorated

@decorationmethod(Buffer)
def set_sub_data(func):
    @ft.wraps(func)
    def decorated(obj, data, *args, **kwargs):
        if isinstance(data, np.ndarray):
            size = data.nbytes
            return func(obj, data, size, *args, **kwargs)
        
        return func(obj, data, *args, **kwargs)
    
    return decorated