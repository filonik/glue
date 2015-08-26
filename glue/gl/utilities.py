from __future__ import absolute_import, division, print_function

import os
import sys

import six

import OpenGL
from OpenGL import GL

_GENERIC_SUFFIX = '.glsl'

_SUFFIX_MAP = {
    ".vs": GL.GL_VERTEX_SHADER, ".vert": GL.GL_VERTEX_SHADER,
    ".tcs": GL.GL_TESS_CONTROL_SHADER, ".tc": GL.GL_TESS_CONTROL_SHADER, ".tesc": GL.GL_TESS_CONTROL_SHADER,
    ".tes": GL.GL_TESS_EVALUATION_SHADER, ".te": GL.GL_TESS_EVALUATION_SHADER, ".tese": GL.GL_TESS_EVALUATION_SHADER,
    ".gs": GL.GL_GEOMETRY_SHADER, ".geom": GL.GL_GEOMETRY_SHADER,
    ".fs": GL.GL_FRAGMENT_SHADER, ".frag": GL.GL_FRAGMENT_SHADER,
    ".cs": GL.GL_COMPUTE_SHADER, ".comp": GL.GL_COMPUTE_SHADER,
}

try:
    import preprocess
    registry = preprocess.getDefaultContentTypesRegistry()
    registry.suffixMap[_GENERIC_SUFFIX] = 'C++'
    for key, value in six.iteritems(_SUFFIX_MAP):
        registry.suffixMap[key] = 'C++'
except ImportError:
    preprocess = None

def application_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), path)

def file_extension_to_shader_type(ext):
    return _SUFFIX_MAP[ext]

def get_shader_type(path):
    _, ext = os.path.splitext(path)
    return file_extension_to_shader_type(ext)

def _get_shader_source_plain(path):
    with open(application_path(path), "r") as f:
        return f.read()

def _get_shader_source_preprocess(path, include_paths=[], defines={}):
    import StringIO
    result = StringIO.StringIO()
    includePath = [application_path(include_path) for include_path in include_paths]
    preprocess.preprocess(application_path(path), result, includePath=includePath, defines=defines, substitute=1)
    return result.getvalue()

def get_shader_source(path, *args, **kwargs):
    if preprocess is not None:
        return _get_shader_source_preprocess(path, *args, **kwargs)
    else:
        return _get_shader_source_plain(path)

def create_textures(image, *args, **kwargs):
    from . import gl
    
    count = kwargs.get("count", 1)
    
    result = [gl.Texture2D(*args, **kwargs) for _ in range(count)]
    
    for texture in result:
        gl.Texture2D.bind(texture)
        texture.set_image(image)
        
    return result
    
def load_textures(path, *args, **kwargs):
    from . import gl
    
    import PIL.Image
    
    image = PIL.Image.open(application_path(path))
    image = image.convert("RGBA")
    
    return create_textures(image, *args, **kwargs)
    
def create_texture(image, *args, **kwargs):
    return create_textures(image, count=1, *args, **kwargs)[0]

def load_texture(path, *args, **kwargs):
    return load_textures(path, count=1, *args, **kwargs)[0]

def load_shader(path, *args, **kwargs):
    from . import gl
    
    type, source = get_shader_type(path), get_shader_source(path)
    
    result = gl.Shader.fromtype(type, *args, **kwargs)
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
