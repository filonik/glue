import contextlib as cl

import OpenGL
from OpenGL import WGL, arrays

def get_current_dc():
    return WGL.wglGetCurrentDC()


# WGL_ARB_extensions_string

def get_extension_string(hdc):
    from OpenGL.WGL.ARB.extensions_string import wglGetExtensionsStringARB
    return wglGetExtensionsStringARB(hdc)


# WGL_EXT_swap_control

def get_swap_interval():
    from OpenGL.WGL.EXT.swap_control import wglGetSwapIntervalEXT
    return wglGetSwapIntervalEXT()

def swap_interval(interval):
    from OpenGL.WGL.EXT.swap_control import wglSwapIntervalEXT
    return wglSwapIntervalEXT(interval)


# WGL_NV_swap_group

def bind_swap_barrier(group, barrier):
    from OpenGL.WGL.NV.swap_group import wglBindSwapBarrierNV
    return wglBindSwapBarrierNV(group, barrier)

def join_swap_group(hdc, group):
    from OpenGL.WGL.NV.swap_group import wglJoinSwapGroupNV
    return wglJoinSwapGroupNV(hdc, group)

def query_frame_count(hdc):
    from OpenGL.WGL.NV.swap_group import wglQueryFrameCountNV
    count = arrays.GLuintArray.zeros((1,))
    if not wglQueryFrameCountNV(hdc, count):
        raise RuntimeError("wglQueryFrameCountNV")
    return count[0]

def query_max_swap_groups(hdc):
    from OpenGL.WGL.NV.swap_group import wglQueryMaxSwapGroupsNV
    nMaxGroups = arrays.GLuintArray.zeros((1,))
    nMaxBarriers = arrays.GLuintArray.zeros((1,))
    if not wglQueryMaxSwapGroupsNV(hdc, nMaxGroups, nMaxBarriers):
        raise RuntimeError("wglQueryMaxSwapGroupsNV")
    return nMaxGroups[0], nMaxBarriers[0]

def query_swap_group(hdc):
    from OpenGL.WGL.NV.swap_group import wglQuerySwapGroupNV
    group = arrays.GLuintArray.zeros((1,))
    barrier = arrays.GLuintArray.zeros((1,))
    if not wglQuerySwapGroupNV(hdc, group, barrier):
        raise RuntimeError("wglQuerySwapGroupNV")
    return group[0], barrier[0]

def reset_frame_count(hdc):
    from OpenGL.WGL.NV.swap_group import wglResetFrameCountNV
    if not wglResetFrameCountNV(hdc):
        raise RuntimeError("wglResetFrameCountNV")
