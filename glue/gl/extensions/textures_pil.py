from __future__ import absolute_import, division, print_function

import functools as ft

import numpy as np
import PIL.Image

from ...decorators import decorationmethod
from ...utilities import Unspecified, specified, getspecified

from ..textures import *

@decorationmethod(Texture2D)
def set_image(func):
    @ft.wraps(func)
    def decorated(obj, image, size=Unspecified, *args, **kwargs):
        if PIL.Image.isImageType(image):
            #image = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
            image = image.convert("RGBA")
            data = np.array(list(image.getdata()), dtype=np.uint8)
            data = np.reshape(data, image.size + (4,))
            return func(obj, data, size=size, *args, **kwargs)
        else:
            return func(obj, image, size=size, *args, **kwargs)
    
    return decorated

@decorationmethod(Texture2D)
def set_sub_image(func):
    @ft.wraps(func)
    def decorated(obj, image, size=Unspecified, *args, **kwargs):
        if PIL.Image.isImageType(image):
            #image = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
            image = image.convert("RGBA")
            data = np.array(list(image.getdata()), dtype=np.uint8)
            data = np.reshape(data, image.size + (4,))
            return func(obj, data, size=size, *args, **kwargs)
        else:
            return func(obj, image, size=size, *args, **kwargs)
    
    return decorated