from __future__ import absolute_import, division, print_function

import functools as ft

import numpy as np
import PIL.Image

from ...decorators import decorationmethod

from ..textures import *

@decorationmethod(Texture2D)
def set_image(func):
    @ft.wraps(func)
    def decorated(obj, image, *args, **kwargs):
        if PIL.Image.isImageType(image):
            #image = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
            image = image.convert("RGBA")
            data = np.array(list(image.getdata()), np.uint8)
            data = np.reshape(data, image.size + (4,))
            return func(obj, data, *args, **kwargs)
        else:
            return func(obj, image, *args, **kwargs)
    
    return decorated