import os
import sys

import contextlib as cl

import numpy as np

import OpenGL
from OpenGL import GL, WGL

from .handles import *
from .shaders import *
from .textures import *


_SHADER_SUFFIX_MAP = {
    ".vs": GL.GL_VERTEX_SHADER, ".vert": GL.GL_VERTEX_SHADER,
    ".tcs": GL.GL_TESS_CONTROL_SHADER, ".tc": GL.GL_TESS_CONTROL_SHADER, ".tesc": GL.GL_TESS_CONTROL_SHADER,
    ".tes": GL.GL_TESS_EVALUATION_SHADER, ".te": GL.GL_TESS_EVALUATION_SHADER, ".tese": GL.GL_TESS_EVALUATION_SHADER,
    ".gs": GL.GL_GEOMETRY_SHADER, ".geom": GL.GL_GEOMETRY_SHADER,
    ".fs": GL.GL_FRAGMENT_SHADER, ".frag": GL.GL_FRAGMENT_SHADER,
    ".cs": GL.GL_COMPUTE_SHADER, ".comp": GL.GL_COMPUTE_SHADER,
}


def shader_type_from_path(path, *args, **kwargs):
    _, extension = os.path.splitext(path)
    return _SHADER_SUFFIX_MAP[extension]

def texture_type_from_path(path, *args, **kwargs):
    # TODO: Support different texture types...
    return GL.GL_TEXTURE_2D


def load(path):
    with open(path, "r") as f: 
        value = f.read()
        return value

def save(path, value):
    with open(path, "w") as f: 
        f.write(value)


def load_source(path):
    import re
    quoted = re.compile('"([^"]*)"')
    
    def _get_include_path(line):
        result = re.search(quoted, line)
        return result.group(1)
    
    def _load_source(path):
        basepath = os.path.dirname(path)
        with open(path, "r") as f: 
            for line in f.readlines():
                if line.startswith("#include"):
                    subpath = os.path.join(basepath, _get_include_path(line))
                    yield from _load_source(subpath)
                else:
                    yield line
    
    result = "".join(_load_source(path))
    
    return result


def create_shader(path, type=None):
    class ShaderData(object):
        pass
    
    def _shader_loader(path, *args, **kwargs):
        result = ShaderData()
        result.source = load_source(path)
        return result
        
    type = shader_type_from_path(path) if type is None else type
    
    data = _shader_loader(path)
    
    result = Shader.from_type(type).create()
    
    result.source(data.source)
    
    result.compile()
    
    if result.compile_status != 1:
        raise Exception("Shader Compile Error:\n%s" % (result.info_log,))
    
    return result


def create_program(shaders, inputs=None, uniforms=None):
    inputs = {} if inputs is None else inputs
    uniforms = {} if uniforms is None else uniforms
    
    result = Program().create()
    
    for shader in shaders:
        result.attach(shader)
    
    result.link()
    
    for shader in shaders:
        result.detach(shader)
    
    if result.link_status != 1:
        raise Exception("Program Link Error:\n%s" % (result.info_log,))
    
    result.inputs = {key: input_setter(result, key, type) for key, type in inputs.items()}
    result.uniforms = {key: uniform_setter(result, key, type) for key, type in uniforms.items()}
    
    return result


def create_texture(path, type=None):
    class TextureData(object):
        pass
    
    def _image_loader(path, *args, **kwargs):
        import PIL.Image
        img = PIL.Image.open(path)
        
        result = TextureData()
        
        result.data = np.array(list(img.getdata()), np.uint8)
        result.size = img.size
        result.format = GL.GL_RGBA
        
        return result
    
    type = texture_type_from_path(path) if type is None else type
    
    data = _image_loader(path)
    
    result = Texture.from_type(type).create()
    
    with bound(result):
        result.image(data.data, data.size, format=data.format)
    
    return result
