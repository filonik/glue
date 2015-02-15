from __future__ import absolute_import, division, print_function

import os
import sys

import six

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

def load_texture(path):
    from . import gl
    
    import PIL.Image
    
    image = PIL.Image.open(os.path.join(application_path(), path))

    result = gl.Texture2D()
    
    gl.Texture2D.bind(result)
    
    result.set_image(image)
    
    return result

def load_shader(path):
    from . import gl
    
    type, source = get_shader_type(path), get_shader_source(path)
    
    result = type()
    result.set_source(source)
    result.compile()
    
    return result

def load_program(paths):
    from . import gl
    
    shaders = [load_shader(path) for path in paths]
    
    result = gl.Program()
    
    for shader in shaders: result.attach(shader)
    
    result.link()
    
    for shader in shaders: result.detach(shader)
    
    return result