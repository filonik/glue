from __future__ import absolute_import, division, print_function

import collections
import contextlib as cl
import copy
import weakref

import six

import cyglfw3 as glfw

from ..decorators import attrcached
from ..flyweights import Resource
from ..utilities import chdir, Unspecified, specified, getspecified

DEFAULT_WINDOW_HINTS = {
    glfw.DECORATED: 1,
    glfw.FOCUSED: 1,
    glfw.RESIZABLE: 1,
    glfw.VISIBLE: 1,
    glfw.FLOATING: 0,
}

DEFAULT_CONTEXT_HINTS = {
    glfw.CONTEXT_VERSION_MAJOR: 4,
    glfw.CONTEXT_VERSION_MINOR: 4,
    glfw.OPENGL_FORWARD_COMPAT: 1,
    glfw.OPENGL_PROFILE: glfw.OPENGL_CORE_PROFILE,
}

def initialize():
    with chdir():
        if not glfw.Init():
            raise Exception('Failed to initialise GLFW.')
        
        from ..gl import gl
        gl._set_backend('glfw')

def terminate():
    glfw.Terminate()

@cl.contextmanager  
def initialized():  
    initialize()
    try:
        yield  
    finally:  
        terminate()

def get_primary_monitor():
    return Monitor(handle=glfw.GetPrimaryMonitor())

def get_monitors():
    return map(lambda handle: Monitor(handle=handle), glfw.GetMonitors())

def poll_events():
    glfw.PollEvents()

class Monitor(Resource):
    __references = dict()
    
    @classmethod
    def references(cls, context=Unspecified):
        return cls.__references
    
    @property
    def video_mode(self):
        return glfw.GetVideoMode(self._handle)
    
    @property
    def position(self):
        return glfw.GetMonitorPos(self._handle)
    
    @property
    def size(self):
        video_mode = self.video_mode
        return (self.video_mode.width, self.video_mode.height)

class Window(Resource):
    __references = dict()
    
    @classmethod
    def references(cls, context=Unspecified):
        return cls.__references
    
    @classmethod
    def create_handle(cls, size, title, monitor=None, share=None, hints=None):
        _hints = {}
        _hints.update(DEFAULT_CONTEXT_HINTS)
        _hints.update(DEFAULT_WINDOW_HINTS)
        _hints.update(hints or {})
        
        for key, value in six.iteritems(_hints):
            glfw.WindowHint(key, value)
        
        return glfw.CreateWindow(size[0], size[1], title, cls.handle(monitor), cls.handle(share))
    
    @classmethod
    def delete_handle(cls, handle):
        glfw.DestroyWindow(handle)
    
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
    
    @property
    @attrcached('__cached_context')
    def context(self):
        return Context(self)
    
    @property
    def position(self):
        return glfw.GetWindowPos(self._handle)
    
    @position.setter
    def position(self, value):
        glfw.SetWindowPos(self._handle, value[0], value[1])
    
    @property
    def size(self):
        return glfw.GetWindowSize(self._handle)
    
    @size.setter
    def size(self, value):
        glfw.SetWindowSize(self._handle, value[0], value[1])
    
    def show(self):
        glfw.ShowWindow(self._handle)
    
    def hide(self):
        glfw.HideWindow(self._handle)
    
    def should_close(self):
        return glfw.WindowShouldClose(self._handle)
    
    def swap_buffers(self):
        glfw.SwapBuffers(self._handle)
        
class Context(Resource):
    __references = dict()
    
    @classmethod
    def references(cls, context=Unspecified):
        return cls.__references
    
    @classmethod
    def create_handle(cls, window):
        return window._handle
    
    @classmethod
    def delete_handle(cls, handle):
        pass
    
    @classmethod
    def get_current(cls):
        handle = glfw.GetCurrentContext()
        return cls(handle=handle)
    
    @classmethod
    def set_current(cls, context):
        glfw.MakeContextCurrent(context._handle)
    
    def __init__(self, *args, **kwargs):
        super(Context, self).__init__(*args, **kwargs)
        
        self._references = collections.defaultdict(dict)
    
    def dispose(self):
        for cls in self._references:
            references = self._references[cls]
            for handle, reference in list(six.iteritems(references)):
                del references[handle]
                cls.delete(handle)
        
        super(Context, self).dispose()
