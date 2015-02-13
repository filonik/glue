from __future__ import absolute_import, division, print_function

import numpy as np

def ortho(l, r, t, b, n, f):
    return np.array([
        [2/(r-l), 0, 0, -(r+l)/(r-l)],
        [0, 2/(b-t), 0, -(b+t)/(b-t)],
        [0, 0, 2/(f-n), -(f+n)/(f-n)],
        [0, 0, 0, 1]
    ], dtype=np.float32)