import math
import time
from . import utils
import itertools
from collections import defaultdict, OrderedDict
from pubsub import pub
from . import Block
BLOCK_SIZE = 2 ** 14


class Piece(object):
    def __init__(self, index, size, data_hash):
        self.index = index
        self.size = size
        self.data_hash = data_hash
        self.files_pending = {}
        self.files_finished = {}
        self.files = []
        self.BLOCK_SIZE = BLOCK_SIZE
        self._blocks = []
        self.has_pending_block = False

    @property
    def blocks(self):
        if not self._blocks:
            num_full_blocks = int(math.floor(float(self.size) / self.BLOCK_SIZE))
            for _ in range(num_full_blocks):
                self._blocks.append(Block.Block(size=self.BLOCK_SIZE, piece=self))
            if (self.size % BLOCK_SIZE) > 0:
                self._blocks.append(Block.Block(size=self.size % BLOCK_SIZE, piece=self))
        return self._blocks

    def set_file(self, filename, data):
        try:
            index = int(self.get_offset(filename) / BLOCK_SIZE)
            offset = int(self.get_offset(filename) % self.BLOCK_SIZE)
        except Exception:
            return
        done = 0
        while done != len(data):
            if offset != 0:
                self.blocks[index].status = "Partial"
                amount = min(self.BLOCK_SIZE - offset, len(data))
            elif len(data) - done < self.blocks[index].size:
                self.blocks[index].status = "Partial"
                amount = len(data) - done
            else:
                self.blocks[index].status = "Full"
                amount = self.blocks[index].size if len(data) - done > self.BLOCK_SIZE else len(data) - done
            self.blocks[index].data[offset] = data[done: done + amount]

            # increment counts
            done += amount
            offset = (offset + amount) % self.BLOCK_SIZE
            index += 1
        self.try_complete()

    def try_complete(self):
        if all([block.status == "Full" or block.status == "Partial" for block in self.blocks]):
            buf = bytearray(b"")
            for index in range(len(self.blocks)):
                buf.extend(self.blocks[index].assemble_data())
            if len(buf) > self.size:
                print("resetting,...")
                self.files_pending = {}
                self.init_blocks()

            if utils.sha1_hash(buf) == self.data_hash:
                for filename in self.files_pending:
                    self.add_file_finished(filename)
                self.files_pending = {}
                self.writeFilesOnDisk(buf)
                pub.sendMessage('PieceManager.update_bitfield', index=self.index)

    def set_block(self, offset, data):
        index = int(offset / BLOCK_SIZE)
        self.blocks[index].data[offset % BLOCK_SIZE] = bytearray(data)
        self.blocks[index].status = "Full"
        self.try_complete()

    def set_all_blocks_pending(self):
        for block in self.blocks:
            block.set_pending()

    def reset_pending_blocks(self):
        for block in self.blocks:
            block.reset_pending()
            self.has_pending_block = False

    def set_file_pending(self, filename):
        self.files_pending[filename] = time.time()

    def remove_file_pending(self, filename):
        try:
            del self.files_pending[filename]
        except KeyError:
            pass

    def add_file_finished(self, filename):
        self.files_finished[filename] = True

    def isCompleteOnDisk(self):
        block_offset = 0
        data = b''
        for f in self.files:
            try:
                f_ptr = open(f["path"], 'rb')
            except IOError:
                break
            f_ptr.seek(f["file_offset"])
            data += f_ptr.read(f["length"])
            f_ptr.close()
            block_offset += f['length']

        if data and utils.sha1_hash(data) == self.data_hash:
            data = bytearray(b'')
            for block in self.blocks:
                block.status = "Full"
            return True
        return False

    def writeFunction(self, pathFile, data, offset):
        try:
            f = open(pathFile, 'r+b')
        except IOError:
            f = open(pathFile, 'wb')
        f.seek(offset)
        f.write(data)
        f.close()

    def writeFilesOnDisk(self, data):
        for f in self.files:
            pathFile = f["path"]
            file_offset = f["file_offset"]
            piece_offset = f["piece_offset"]
            length = f["length"]
            self.writeFunction(pathFile, data[piece_offset: piece_offset + length], file_offset)
        for block in self.blocks:
            block.data = {0: bytearray(b'')}

    def get_file_offset(self, filename):
        for f in self.files:
            if f.get('path').split('/')[-1] == filename:
                return f.get('file_offset')

    def get_length(self, filename):
        for f in self.files:
            if f.get('path').split('/')[-1] == filename:
                return f.get('length')

    def get_offset(self, filename):
        for f in self.files:
            if f.get('path').split('/')[-1] == filename:
                return math.floor(f.get('piece_offset'))
