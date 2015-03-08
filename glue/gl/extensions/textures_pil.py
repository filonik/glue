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
            size = getspecified(size, image.size)
            image = np.array(list(image.getdata()), dtype=np.uint8)
            image = np.reshape(image, (size[1], size[0], 4))
            return func(obj, image, size, *args, **kwargs)
        else:
            return func(obj, image, size, *args, **kwargs)
    
    return decorated

@decorationmethod(Texture2D)
def set_sub_image(func):
    @ft.wraps(func)
    def decorated(obj, image, size=Unspecified, *args, **kwargs):
        if PIL.Image.isImageType(image):
            #image = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
            image = image.convert("RGBA")
            size = getspecified(size, image.size)
            image = np.array(list(image.getdata()), dtype=np.uint8)
            image = np.reshape(image, (size[1], size[0], 4))
            return func(obj, image, size, *args, **kwargs)
        else:
            return func(obj, image, size, *args, **kwargs)
    
    return decorated