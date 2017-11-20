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
    
    def create(self, context):
        from glue.gl import utilities
        
        self._program = utilities.load_program([
            "examples/data/shaders/noop.vs",
            "examples/data/shaders/quad.gs",
            "examples/data/shaders/quad.fs",
        ], uniforms={
            "iChannel0": gl.Sampler2DType,
            "iChannel1": gl.Sampler2DType,
            "iResolution": gl.Vec3Type,
            "iTime": gl.ScalarType,
        })
        
        self._vao = gl.VertexArray().create()
    
    def render(self, context):
        gl.clear_color(self._background)
        gl.clear()
        
        with gl.bound(self._program), gl.bound(self._vao):
            self._program.uniforms["iResolution"] = np.array(context.resolution, dtype=np.float32)
            self._program.uniforms["iTime"] = context.time
            
            GL.glDrawArrays(GL.GL_POINTS, 0, 1)


if __name__ == '__main__':
    app = backend.Application(sys.argv)
    
    window = backend.Window(ExampleScene())
    window.setTitle("Hello glue!")
    window.resize(1280, 720)
    window.show()
    
    sys.exit(app.main())

