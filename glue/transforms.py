from __future__ import absolute_import, division, print_function

import numpy as np

DEFAULT_SIZE = 4

def identity(n=DEFAULT_SIZE):
    return np.identity(n, dtype=np.float32)

def translate(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def scale(x, y, z):
    return np.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def shear(x, y, z):
    return np.array([
        [1, 0, x, 0],
        [0, 1, y, 0],
        [0, 0, 1, 0],
        [0, 0, z, 1]
    ], dtype=np.float32)
