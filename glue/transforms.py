from __future__ import absolute_import, division, print_function

import numpy as np

DEFAULT_SIZE = 4

def quaternion_from_axis_angle(v, a):
    sin_a_half = np.sin(a/2.0)
    cos_a_half = np.cos(a/2.0)
    axis = v * (sin_a_half/np.linalg.norm(v))
    return np.r_[axis, cos_a_half]

def identity(n=DEFAULT_SIZE):
    return np.identity(n, dtype=np.float32)

def orientate(x, y, z, w):
    return np.array([
        [(1-(2*y*y))-(2*z*z), (2*x*y)-(2*z*w), (2*x*z)+(2*y*w), 0],
        [(2*x*y)+(2*z*w), (1-(2*x*x))-(2*z*z), (2*y*z)-(2*x*w), 0],
        [(2*x*z)-(2*y*w), (2*y*z)+(2*x*w), (1-(2*x*x))-(2*y*y), 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def translate(x, y, z):
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [x, y, z, 1]
    ], dtype=np.float32)

def scale(x, y, z):
    return np.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def transform(o, t, s):
    return np.tensordot(scale(*s), translate(*t), axes=1)

def shear(x, y, z):
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [x, y, 1, z],
        [0, 0, 0, 1]
    ], dtype=np.float32)
