from __future__ import print_function

import collections
import logging

DEFAULT_PAST_FRAME_THRESHOLD = 10

CURSOR_ATTRIBUTES = ['session_id', 'position', 'velocity', 'acceleration']
OBJECT_ATTRIBUTES = ['session_id', 'fiducial_id', 'position', 'angle', 'velocity', 'rotation_speed', 'acceleration', 'rotation_acceleration']

class Cursor2D(collections.namedtuple('Cursor2D', CURSOR_ATTRIBUTES)):
    @classmethod
    def frommessage(cls, path, args, types, src):
        assert path == "/tuio/2Dcur"
        return cls(args[1], args[2:4], args[4:6], args[6])

class Cursor25D(collections.namedtuple('Cursor25D', CURSOR_ATTRIBUTES)):
    @classmethod
    def frommessage(cls, path, args, types, src):
        assert path == "/tuio/25Dcur"
        return cls(args[1], args[2:5], args[5:8], args[8])

class Object2D(collections.namedtuple('Object2D', OBJECT_ATTRIBUTES)):
    @classmethod
    def frommessage(cls, path, args, types, src):
        assert path == "/tuio/2Dobj"
        return cls(args[1], args[2], args[3:5], args[5], args[6:8], args[8], args[9], args[10])
        
class Object25D(collections.namedtuple('Object25D', OBJECT_ATTRIBUTES)):
    @classmethod
    def frommessage(cls, path, args, types, src):
        assert path == "/tuio/25Dobj"
        return cls(args[1], args[2], args[3:6], args[6], args[7:10], args[10], args[11], args[12])

class Listener(object):
    def __init__(self, *args, **kwargs):
        super(Listener, self).__init__(*args, **kwargs)
        
        self.sources = set()
        
        self.instances = collections.defaultdict(dict)
        
        self.creates = collections.defaultdict(list)
        self.updates = collections.defaultdict(list)
        self.deletes = collections.defaultdict(list)
        
        self.last_frames = dict()
        
        self.create_callback = None
        self.update_callback = None
        self.delete_callback = None
    
    def attach(self, server):
        server.add_method("/tuio/2Dcur", None, self._tuio_2Dcur_callback)
        server.add_method("/tuio/25Dcur", None, self._tuio_25Dcur_callback)
        server.add_method("/tuio/2Dobj", None, self._tuio_2Dobj_callback)
        server.add_method("/tuio/25Dobj", None, self._tuio_25Dobj_callback)
    
    def detach(self, server):
        server.del_method("/tuio/2Dcur", None)
        server.del_method("/tuio/25Dcur", None)
        server.del_method("/tuio/2Dobj", None)
        server.del_method("/tuio/25Dobj", None)
    
    def generic_message_handler(self, cls, path, args, types, src, data):
        cmd = args[0] if len(args) else None
        src = src.url
        
        self.sources.add(src)
        if cmd == 'set':
            obj = cls.frommessage(path, args, types, src)
            if obj.session_id in self.instances[src]:
                self.updates[src].append(obj)
            else:
                self.creates[src].append(obj)
        elif cmd == 'alive':
            for sid in self.instances[src]:
                if sid not in args[1:]:
                    self.deletes[src].append(sid)
        elif cmd == 'fseq':
            frame, last_frame = args[1], self.last_frames.get(src, 0)
            frame_delta = frame - last_frame
            
            if frame == -1 or 0 < frame_delta or frame_delta < -DEFAULT_PAST_FRAME_THRESHOLD:
                for obj in self.creates[src]:
                    self.instances[src][obj.session_id] = obj
                    if self.create_callback is not None: self.create_callback(obj)
                    
                for obj in self.updates[src]:
                    self.instances[src][obj.session_id] = obj
                    if self.update_callback is not None: self.update_callback(obj)
                    
                for sid in self.deletes[src]:
                    obj = self.instances[src].pop(sid)
                    if self.delete_callback is not None: self.delete_callback(obj)
                
                self.last_frames[src] = last_frame if frame == -1 else frame
            
            del self.creates[src][:]
            del self.updates[src][:]
            del self.deletes[src][:]
        elif cmd == 'source':
            pass
        else:
            logging.warn('Unexpected command "%s %s".' % (path, cmd,))
    
    def _tuio_2Dcur_callback(self, *args, **kwargs):
        self.generic_message_handler(Cursor2D, *args, **kwargs)
    
    def _tuio_25Dcur_callback(self, *args, **kwargs):
        self.generic_message_handler(Cursor25D, *args, **kwargs)
        
    def _tuio_2Dobj_callback(self, *args, **kwargs):
        self.generic_message_handler(Object2D, *args, **kwargs)
    
    def _tuio_25Dobj_callback(self, *args, **kwargs):
        self.generic_message_handler(Object25D, *args, **kwargs)