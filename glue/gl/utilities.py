from __future__ import absolute_import, division, print_function

import os
import sys

import six

import OpenGL
from OpenGL import GL

def application_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def file_extension_to_shader_type(ext):
    from . import gl
    return {
        ".vs": gl.VertexShader, ".vert": gl.VertexShader,
        ".tc": gl.TessellationControlShader, ".tesc": gl.TessellationControlShader,
        ".te": gl.TessellationEvaluationShader, ".tese": gl.TessellationEvaluationShader,
        ".gs": gl.GeometryShader, ".geom": gl.GeometryShader,
        ".fs": gl.FragmentShader, ".frag": gl.FragmentShader,
    }[ext]

def get_shader_type(path):
    _, ext = os.path.splitext(path)
    return file_extension_to_shader_type(ext)
    
def get_shader_source(path):
    with open(os.path.join(application_path(), path), "r") as f:
        return f.read()

def load_texture(path, *args, **kwargs):
    from . import gl
    
    import PIL.Image
    
    image = PIL.Image.open(os.path.join(application_path(), path))

    result = gl.Texture2D(*args, **kwargs)
    
    gl.Texture2D.bind(result)
    
    result.set_image(image)
    
    return result

def load_shader(path, *args, **kwargs):
    from . import gl
    
    type, source = get_shader_type(path), get_shader_source(path)
    
    result = type(*args, **kwargs)
    result.set_source(source)
    result.compile()
    
    return result

def load_program(paths, *args, **kwargs):
    from . import gl
    
    shaders = [load_shader(path, *args, **kwargs) for path in paths]
    
    result = gl.Program(*args, **kwargs)
    
    for shader in shaders: result.attach(shader)
    
    result.link()
    
    for shader in shaders: result.detach(shader)
    
    return result

def save_screenshot(path):
    from . import gl
    
    import PIL.Image
    
    _, _, w, h = GL.glGetIntegerv(GL.GL_VIEWPORT)
    
    GL.glReadBuffer(GL.GL_FRONT)
    data = GL.glReadPixels(0, 0, w, h, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)
    
    image = PIL.Image.fromstring(mode="RGBA", size=(w, h), data=data)     
    image = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
    image.save(path, 'PNG')
