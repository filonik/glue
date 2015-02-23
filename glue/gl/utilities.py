from __future__ import absolute_import, division, print_function

import os
import sys

import six

import OpenGL
from OpenGL import GL

_TYPE_MAP = {
    ".vs": GL.GL_VERTEX_SHADER, ".vert": GL.GL_VERTEX_SHADER,
    ".cs": GL.GL_TESS_CONTROL_SHADER, ".tc": GL.GL_TESS_CONTROL_SHADER, ".tesc": GL.GL_TESS_CONTROL_SHADER,
    ".es": GL.GL_TESS_EVALUATION_SHADER, ".te": GL.GL_TESS_EVALUATION_SHADER, ".tese": GL.GL_TESS_EVALUATION_SHADER,
    ".gs": GL.GL_GEOMETRY_SHADER, ".geom": GL.GL_GEOMETRY_SHADER,
    ".fs": GL.GL_FRAGMENT_SHADER, ".frag": GL.GL_FRAGMENT_SHADER,
}

try:
    import preprocess
    registry = preprocess.getDefaultContentTypesRegistry()
    registry.suffixMap['glsl'] = 'C++'
    for key, value in six.iteritems(_TYPE_MAP):
        registry.suffixMap[key[1:]] = 'C++'
except ImportError:
    preprocess = None

def application_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def file_extension_to_shader_type(ext):
    return _TYPE_MAP[ext]

def get_shader_type(path):
    _, ext = os.path.splitext(path)
    return file_extension_to_shader_type(ext)

def _get_shader_source_plain(path):
    with open(os.path.join(application_path(), path), "r") as f:
        return f.read()

def _get_shader_source_preprocess(path, include_paths=[], defines={}):
    import StringIO
    result = StringIO.StringIO()
    preprocess.preprocess(os.path.join(application_path(), path), result, includePath=include_paths, defines=defines)
    return result.getvalue()

def get_shader_source(path, *args, **kwargs):
    if preprocess is not None:
        return _get_shader_source_preprocess(path, *args, **kwargs)
    else:
        return _get_shader_source_plain(path)

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
