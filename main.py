#! /usr/bin/python2

from __future__ import absolute_import, division, print_function

import math
import time

import numpy as np

from glue import glfw, gl, projections, transforms
from glue.gl import GL, utilities

import logging
logging.basicConfig(filename='glue.log', level=logging.DEBUG)

def rect(w=1.0, h=1.0):
    data = np.zeros(4, dtype = [
        ("position", np.float32, 3),
        ("color", np.float32, 4),
        ("texCoord", np.float32, 2),
        ("normal", np.float32, 3),
    ])
    
    w_half, h_half = w/2.0, h/2.0
    
    data['position'] = [ (-w_half, -h_half, 0), (-w_half, +h_half, 0), (+w_half, -h_half, 0), (+w_half, +h_half, 0) ]
    data['color'] = [ (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1) ]
    data['texCoord'] = [ (0, 0), (0, +1), (+1, 0), (+1, +1) ]
    data['normal'] = [ (+1, 0, 0), (+1, 0, 0), (+1, 0, 0), (+1, 0, 0) ]
    
    return data

def info():
    print('GLFW Version: %s' % (glfw.glfw.GetVersionString(),))
    print("GL Version: %s" % (GL.glGetString(GL.GL_VERSION),))
    print("GLSL Version: %s\n" % (GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION),))

program = None
vao = None
vbo = None

def init(window):
    global program, vao, vbo
    
    program = utilities.load_program([
        'data/shader/plain.vs',
        'data/shader/plain.fs',
    ])
    
    vao = gl.VertexArrayObject()
    gl.VertexArrayObject.bind(vao)
    
    vbo = gl.VertexBufferObject()
    gl.VertexBufferObject.bind(vbo)
    vbo.set_data(rect())

def render(window):
    global program, vao, vbo
    
    gl.clear_color([1.0,1.0,1.0])
    gl.clear()
    
    gl.Program.bind(program)
    
    size = np.asarray(window.size)
    aspect = size / np.min(size)
    
    projection = projections.ortho(-aspect[0], +aspect[0], -aspect[1], +aspect[1], -1.0, +1.0)
    model_view = transforms.translate(0, np.sin(2*np.pi*math.fmod(time.time(), 5.0)/5.0), 0)
    
    program.uniforms['projection'] = projection
    program.uniforms['model_view'] = model_view
    
    program.attributes['position'] = vbo
    program.attributes['color'] = vbo
    
    GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 0, vbo.type.dtype['position'].size)

def main():
    window = glfw.Window((800, 600), "Hello GLUE!")
    glfw.Context.set_current(window.context)
    
    info()
    
    init(window)
    
    gl.cleanup()
    
    while not window.should_close():
        glfw.poll_events()
        
        render(window)
        
        gl.cleanup()
        
        window.swap_buffers()
    
    window.dispose()

if __name__ == "__main__":
    with glfw.initialized():
        main()