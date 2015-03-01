from __future__ import absolute_import, division, print_function

import numpy as np

def ortho(l, r, t, b, n, f):
    return np.array([
        [2/(r-l), 0, 0, 0],
        [0, 2/(b-t), 0, 0],
        [0, 0, 2/(f-n), 0],
        [-(r+l)/(r-l), -(b+t)/(b-t), -(f+n)/(f-n), 1]
    ], dtype=np.float32)
    
def frustum(l, r, t, b, n, f):
    return np.array([
        [2*(n/(r-l)), 0, 0, 0],
        [0, 2*(n/(t-b)), 0, 0],
        [(r + l)/(r - l), (t + b)/(t - b), -1*(f + n)/(f - n), -1],
        [0, 0, -2*((f * n)/(f - n)), 0]
    ], dtype=np.float32)