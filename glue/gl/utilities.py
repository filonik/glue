from __future__ import absolute_import, division, print_function

import os
import sys

import six

from . import gl

def application_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def file_extension_to_shader_type(ext):
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

def load_shader(path):
    type, source = get_shader_type(path), get_shader_source(path)
    
    result = type()
    result.set_source(source)
    result.compile()
    
    return result

def load_program(paths):
    shaders = [load_shader(path) for path in paths]
    
    result = gl.Program()
    
    for shader in shaders: result.attach(shader)
    
    result.link()
    
    for shader in shaders: result.detach(shader)
    
    return result