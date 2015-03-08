from __future__ import absolute_import, division, print_function

import functools as ft

import numpy as np

from ...decorators import decorationmethod
from ...utilities import Unspecified, specified, getspecified

from ..textures import *

from .types_numpy import _nptypes_to_gltypes

@decorationmethod(Texture2D)
def set_image(func):
    @ft.wraps(func)
    def decorated(obj, image, size=Unspecified, type=Unspecified, format=Unspecified, *args, **kwargs):
        if isinstance(image, np.ndarray):
            size = getspecified(size, (image.shape[1], image.shape[0]))
            type = getspecified(type, _nptypes_to_gltypes[image.dtype.type])
            format = getspecified(format, DEFAULT_TEXTURE_FORMATS.get(image.shape[2], DEFAULT_TEXTURE_FORMAT))
            image = np.flipud(image)
            return func(obj, image, size, type, format=format, *args, **kwargs)
        else:
            return func(obj, image, size, type, format=format, *args, **kwargs)
    
    return decorated

@decorationmethod(Texture2D)
def set_sub_image(func):
    @ft.wraps(func)
    def decorated(obj, image, size=Unspecified, type=Unspecified, format=Unspecified, *args, **kwargs):
        if isinstance(image, np.ndarray):
            size = getspecified(size, (image.shape[1], image.shape[0]))
            type = getspecified(type, _nptypes_to_gltypes[image.dtype.type])
            format = getspecified(format, DEFAULT_TEXTURE_FORMATS.get(image.shape[2], DEFAULT_TEXTURE_FORMAT))
            image = np.flipud(image)
            return func(obj, image, size, type, format=format, *args, **kwargs)
        else:
            return func(obj, image, size, type, format=format, *args, **kwargs)
    
    return decorated