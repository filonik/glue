import os
import sys

import numpy as np

from glue import gl
from glue.gl import GL

import backend


class ExampleScene(backend.Scene):
    def __init__(self):
        self._background = np.array([1,0,0,0], dtype=np.float32)
        self._foreground = np.array([0,0,0,0], dtype=np.float32)

    def render(self, context):
        gl.clear_color(self._background)
        gl.clear()


if __name__ == '__main__':
    app = backend.Application(sys.argv)
    
    window = backend.Window(ExampleScene())
    window.setTitle("Hello glue!")
    window.resize(1280, 720)
    window.show()
    
    sys.exit(app.main())

