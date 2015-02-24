from __future__ import absolute_import, division, print_function

import collections
import contextlib as cl
import copy
import weakref

import six

import cyglfw3 as GLFW

from ..decorators import attrcached
from ..flyweights import Resource
from ..utilities import chdir, Unspecified, specified, getspecified

DEFAULT_WINDOW_HINTS = {
    GLFW.DECORATED: 1,
    GLFW.FOCUSED: 1,
    GLFW.RESIZABLE: 1,
    GLFW.VISIBLE: 1,
    GLFW.FLOATING: 0,
}

DEFAULT_CONTEXT_HINTS = {
    GLFW.CONTEXT_VERSION_MAJOR: 4,
    GLFW.CONTEXT_VERSION_MINOR: 4,
    GLFW.OPENGL_FORWARD_COMPAT: 1,
    GLFW.OPENGL_PROFILE: GLFW.OPENGL_CORE_PROFILE,
}

def initialize():
    with chdir():
        if not GLFW.Init():
            raise Exception('Failed to initialise GLFW.')
        
        from ..gl import gl
        gl._set_backend('glfw')

def terminate():
    GLFW.Terminate()

@cl.contextmanager  
def initialized():  
    initialize()
    try:
        yield  
    finally:  
        terminate()

def get_primary_monitor():
    return Monitor(handle=GLFW.GetPrimaryMonitor())

def get_monitors():
    return map(lambda handle: Monitor(handle=handle), GLFW.GetMonitors())

def poll_events():
    GLFW.PollEvents()

class Monitor(Resource):
    __references = dict()
    
    @classmethod
    def references(cls, context=Unspecified):
        return cls.__references
    
    @property
    def video_mode(self):
        return GLFW.GetVideoMode(self._handle)
    
    @property
    def position(self):
        return GLFW.GetMonitorPos(self._handle)
    
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
            GLFW.WindowHint(key, value)
        
        return GLFW.CreateWindow(size[0], size[1], title, cls.handle(monitor), cls.handle(share))
    
    @classmethod
    def delete_handle(cls, handle):
        GLFW.DestroyWindow(handle)
    
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
    
    @property
    @attrcached('__cached_context')
    def context(self):
        return Context(self)
    
    @property
    def position(self):
        return GLFW.GetWindowPos(self._handle)
    
    @position.setter
    def position(self, value):
        GLFW.SetWindowPos(self._handle, value[0], value[1])
    
    @property
    def size(self):
        return GLFW.GetWindowSize(self._handle)
    
    @size.setter
    def size(self, value):
        GLFW.SetWindowSize(self._handle, value[0], value[1])
    
    def show(self):
        GLFW.ShowWindow(self._handle)
    
    def hide(self):
        GLFW.HideWindow(self._handle)
    
    def should_close(self):
        return GLFW.WindowShouldClose(self._handle)
    
    def swap_buffers(self):
        GLFW.SwapBuffers(self._handle)
        
    def set_window_size_callback(self, on_window_size):
        GLFW.SetWindowSizeCallback(self._handle, on_window_size)
    
    def set_framebuffer_size_callback(self, on_size):
        GLFW.SetFramebufferSizeCallback(self._handle, on_framebuffer_size)
    
    def set_mouse_button_callback(self, on_mouse_button):
        GLFW.SetMouseButtonCallback(self._handle, on_mouse_button)
    
    def set_scroll_callback(self, on_mouse_wheel):
        GLFW.SetScrollCallback(self._handle, on_mouse_wheel)
    
    def set_cursor_pos_callback(self, on_mouse_move):
        GLFW.SetCursorPosCallback(self._handle, on_mouse_move)
    
    def set_key_callback(self, on_keyboard_key):
        GLFW.SetKeyCallback(self._handle, on_keyboard_key)
    
    on_mouse_button = set_mouse_button_callback
    on_mouse_wheel = set_scroll_callback
    on_mouse_move = set_cursor_pos_callback
    on_keyboard_key = set_key_callback    
    

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
        handle = GLFW.GetCurrentContext()
        return cls(handle=handle)
    
    @classmethod
    def set_current(cls, context):
        GLFW.MakeContextCurrent(context._handle)
    
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
