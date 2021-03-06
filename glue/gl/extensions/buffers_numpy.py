from __future__ import absolute_import, division, print_function

import functools as ft

import numpy as np

from ...decorators import decorationmethod
from ...utilities import Unspecified, specified, getspecified

from ..buffers import *

@decorationmethod(Buffer)
def set_data(func):
    @ft.wraps(func)
    def decorated(obj, data, size=Unspecified, *args, **kwargs):
        if isinstance(data, np.ndarray):
            size = getspecified(size, data.nbytes)
            return func(obj, data, size, *args, **kwargs)
        
        return func(obj, data, size, *args, **kwargs)
    
    return decorated

@decorationmethod(Buffer)
def get_sub_data(func):
    @ft.wraps(func)
    def decorated(obj, data, size=Unspecified, *args, **kwargs):
        if isinstance(data, np.ndarray):
            size = getspecified(size, data.nbytes)
            return func(obj, data, size, *args, **kwargs)
        
        return func(obj, data, size, *args, **kwargs)
    
    return decorated

@decorationmethod(Buffer)
def set_sub_data(func):
    @ft.wraps(func)
    def decorated(obj, data, size=Unspecified, *args, **kwargs):
        if isinstance(data, np.ndarray):
            size = getspecified(size, data.nbytes)
            return func(obj, data, size, *args, **kwargs)
        
        return func(obj, data, size, *args, **kwargs)
    
    return decorated