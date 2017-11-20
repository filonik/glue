import time

import logging

from PyQt5 import QtCore, QtGui, QtNetwork
from PyQt5.QtCore import Qt


class Scene(object):
    def create(self, context):
        pass
    
    def update(self, context):
        pass
    
    def render(self, context):
        pass
    
    def delete(self, context):
        pass


class Window(QtGui.QOpenGLWindow):
    @property
    def fullscreen(self):
        return self._fullscreen
    
    @fullscreen.setter
    def fullscreen(self, value):
        self._fullscreen = value
        (self.enableFullscreen if self.video.fullscreen else self.disableFullscreen)()
    
    @property
    def resolution(self):
        return [self.width(), self.height(), 1]
    
    @property
    def time(self):
        return self._time - self._startTime
    
    def __init__(self, scene=None):
        super().__init__()
        
        self._active = True
        self._fullscreen = False
        
        self._scene = scene
        
        format = QtGui.QSurfaceFormat()
        format.setProfile(QtGui.QSurfaceFormat.CoreProfile)
        format.setVersion(4, 4)
        
        self.setFormat(format)
    
    def enableFullscreen(self):
        QtGui.QGuiApplication.setOverrideCursor(Qt.BlankCursor)
        self.showFullScreen()
    
    def disableFullscreen(self):
        self.showNormal()
        QtGui.QGuiApplication.restoreOverrideCursor()
    
    def initializeGL(self):
        self._time = time.time()
        self._startTime = self._time
        
        if self._scene:
            self._scene.create(self)
    
    def paintGL(self):
        self._time = time.time()
        
        if self._scene:
            self._scene.update(self)
            self._scene.render(self)
        
        if self._active:
            self.requestUpdate()
    
    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            QtGui.QGuiApplication.instance().quit()
        elif event.key() == Qt.Key_Return:
            if event.modifiers() & Qt.AltModifier:
                self.toggleFullscreen()


class Application(QtGui.QGuiApplication):
    def main(self):
        try:
            result = -1
            result = self.exec_()
        except Exception as e:
            logging.exception("Uncaught Exception")
        finally:
            return result
