from __future__ import print_function

import functools as ft
import threading

import liblo

import logging
log = logging.getLogger(__name__)

class ThreadedServer(liblo.Server):
    def __init__(self, port=3333, timeout=100):
        super(ThreadedServer, self).__init__(port)
        self.stoprequest = threading.Event()
        self.thread = threading.Thread(target=ft.partial(self.run, timeout))
        self.thread.daemon = True
        self.timeout = 100
    
    def attach(self, listener):
        listener.attach(self)
    
    def detach(self, listener):
        listener.attach(self)
    
    def run(self, timeout=None):
        log.info("Server started.")
        while not self.stoprequest.is_set():
            self.recv(self.timeout)
        log.info("Server stopped.")
    
    def start(self):
        self.thread.start()
    
    def stop(self, timeout=None):
        self.stoprequest.set()
        self.thread.join(timeout)