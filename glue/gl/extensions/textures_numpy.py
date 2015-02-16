from __future__ import absolute_import, division, print_function

import functools as ft

import numpy as np

from ...decorators import decorationmethod

from ..textures import *

from .types_numpy import _nptypes_to_gltypes

@decorationmethod(Texture2D)
def set_image(func):
    @ft.wraps(func)
    def decorated(obj, image, *args, **kwargs):
        if isinstance(image, np.ndarray):
            size = image.shape
            type = _nptypes_to_gltypes[image.dtype.type]
            image = np.flipud(image)
            return func(obj, image, size, type, *args, **kwargs)
        else:
            return func(obj, image, *args, **kwargs)
    
    return decorated

@decorationmethod(Texture2D)
def set_sub_image(func):
    @ft.wraps(func)
    def decorated(obj, image, *args, **kwargs):
        if isinstance(image, np.ndarray):
            size = image.shape
            type = _nptypes_to_gltypes[image.dtype.type]
            image = np.flipud(image)
            return func(obj, image, size, type, *args, **kwargs)
        else:
            return func(obj, image, *args, **kwargs)
    
    return decorated