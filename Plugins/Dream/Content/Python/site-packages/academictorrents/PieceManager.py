from . import Piece
import bitstring
import time
import math
from pubsub import pub
from collections import defaultdict
from tqdm import tqdm

class PieceManager(object):
    def __init__(self, torrent):
        self.torrent = torrent
        self.number_of_pieces = torrent.number_of_pieces
        self.bitfield = bitstring.BitArray(self.number_of_pieces)
        self.pieces = self.generate_pieces()
        self.files = self.get_files()
        for f in self.files:
            id_piece = f['id_piece']
            self.pieces[id_piece].files.append(f)

        # Create events
        pub.subscribe(self.receive_block, 'PieceManager.receive_block')
        pub.subscribe(self.receive_file, 'PieceManager.receive_file')
        pub.subscribe(self.update_bitfield, 'PieceManager.update_bitfield')


    def close(self):
        pub.unsubAll("PieceManager.receive_block")
        pub.unsubAll("PieceManager.receive_file")
        pub.unsubAll("PieceManager.update_bitfield")
        self.torrent = None
        self.bitfield = None
        self.pieces = None
        self.files = None

    def finished(self):
        if sum(self.bitfield) == self.number_of_pieces:
            return True
        return False

    def check_finished_pieces(self):
        b = 0
        for i in range(self.number_of_pieces):
            if self.bitfield[i]:
                b += self.pieces[i].size
        return b

    def check_full_blocks(self):
        b = 0
        for piece in self.pieces:
            for block in piece.blocks:
                if block.status == "Full":
                    b += block.size
        return b

    def update_bitfield(self, index):
        self.bitfield[index] = 1

    def receive_block(self, piece):
        index, offset, data = piece
        self.pieces[index].set_block(offset, data)

    def receive_file(self, piece):
        index, filename, data = piece
        try:
            self.pieces[index].set_file(filename, data)
        except Exception:
            pass

    def reset_pending(self):
        for piece in self.pieces:
            if piece.has_pending_block:
                piece.reset_pending_blocks()
                piece.has_pending_block = False

    def set_pending(self, filename, pieces):
        for piece in pieces:
            cur = int(math.floor(piece.get_offset(filename)/piece.BLOCK_SIZE))
            last = int(math.floor((piece.get_length(filename) + piece.get_offset(filename))/piece.BLOCK_SIZE))
            piece.set_file_pending(filename)
            while cur < last:
                piece.blocks[cur].set_pending()
                cur += 1

    def pieces_by_file(self, reverse=False):
        pieces_by_file = defaultdict(list)
        pieces = [piece for index, piece in enumerate(self.pieces) if not self.bitfield[index]]
        for piece in pieces:
            for f in piece.files:
                filename = f.get('path').split('/')[-1]
                timestamp = piece.files_pending.get(filename, 0)
                if int(time.time() - timestamp) > 1 and filename not in piece.files_finished.keys():
                    pieces_by_file[filename].append(piece)
        sorted_by_length = sorted(pieces_by_file.items(), key=lambda k_v: len(k_v[1]), reverse=reverse)
        return sorted_by_length

    def check_disk_pieces(self):
        print("Checking pieces on disk...")
        for i in tqdm(range(0, self.number_of_pieces)):
            self.bitfield[i] = self.pieces[i].isCompleteOnDisk()  # this should set all the finished bools on the finished pieces
        print("Found " + str(sum(self.bitfield)) + " finished pieces out of " + str(len(self.bitfield)) + " total pieces.")

    def generate_pieces(self):
        pieces = []
        for i in range(self.number_of_pieces):
            start = i * 20
            end = start + 20

            if i == (self.number_of_pieces - 1):
                length = self.torrent.total_length - (self.number_of_pieces-1) * self.torrent.piece_length
                pieces.append(Piece.Piece(i, length, self.torrent.pieces[start:end]))
            else:
                pieces.append(Piece.Piece(i, self.torrent.piece_length, self.torrent.pieces[start:end]))
        return pieces

    def get_files(self):
        files = []
        piece_offset = 0
        size_used = 0

        for f in self.torrent.filenames:

            current_size_file = f["length"]
            file_offset = 0

            while current_size_file > 0:
                id_piece = int(piece_offset / self.torrent.piece_length)
                size = self.pieces[id_piece].size - size_used

                if current_size_file - size < 0:
                    file = {"length": current_size_file,"id_piece":id_piece ,"file_offset":file_offset, "piece_offset":size_used ,"path":f["path"]}
                    piece_offset += current_size_file
                    file_offset += current_size_file
                    size_used += current_size_file
                    current_size_file = 0

                else:
                    current_size_file -= size
                    file = {"length":size,"id_piece":id_piece ,"file_offset":file_offset,"piece_offset":size_used , "path":f["path"]}
                    piece_offset += size
                    file_offset += size
                    size_used = 0

                files.append(file)
        return files
