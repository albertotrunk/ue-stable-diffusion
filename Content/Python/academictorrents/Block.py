import time
from collections import defaultdict

class Block(object):
    def __init__(self, size, time=time.time(), status="Free", data=None, piece=None):
        self.size = size
        self.status = status
        self.pending = False
        self.data = defaultdict(list)
        self.time = time
        self.piece = piece

    def assemble_data(self):
        buf = bytearray(self.size)
        length = 0
        for index, data in self.data.items():
            index = int(index % self.size)
            buf[index: index + len(data)] = data
            length += len(data)
        if length != self.size:
            return bytearray(b"")
        return buf

    def set_pending(self):
        self.pending = True
        self.time = int(time.time())
        self.piece.has_pending_block = True

    def reset_pending(self):
        if(int(time.time()) - self.time) > 8:
            self.pending = False
            self.time = 0
