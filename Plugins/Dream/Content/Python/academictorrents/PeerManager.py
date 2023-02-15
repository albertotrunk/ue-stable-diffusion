import select
import struct
from queue import Queue
try:
    from itertools import zip_longest as zip_longest
except:
    from itertools import izip_longest as zip_longest
import time
import logging
from threading import Thread
from pubsub import pub
from . import utils
from . import RarestPieces
from .HttpPeer import HttpPeer


class PeerManager(Thread):
    def __init__(self, urls, piece_manager, request_queue):
        Thread.__init__(self)
        self.peers = []
        self.http_peers = []
        self.request_queue = request_queue
        self.piece_manager = piece_manager
        self.rarestPieces = RarestPieces.RarestPieces(piece_manager)
        self.stop_requested = False

        self.pieces_by_peer = []
        for i in range(self.piece_manager.number_of_pieces):
            self.pieces_by_peer.append([0, []])
        for url in urls:
            self.http_peers.append(HttpPeer(url))

        # Events
        pub.subscribe(self.add_peer, 'PeerManager.new_peer')
        pub.subscribe(self.peers_bitfield, 'PeerManager.update_peers_bitfield')

    def run(self):
        while not self.stop_requested:
            self.start_connection_to_peers()
            read = [p.socket for p in self.peers]
            readList, _, _ = select.select(read, [], [], 1)

            # Receive from peers
            for socket in readList:
                peer = self.get_peer_by_socket(socket)
                try:
                    msg = socket.recv(1024)
                except Exception as e:
                    logging.info(peer.ip + ": removing peer because of: " + str(e))
                    self.remove_peer(peer)
                    continue

                if not msg:
                    logging.error(peer.ip + ": removing peer because we received a message of 0 length")
                    self.remove_peer(peer)
                    continue

                peer.buffer += msg

                if not peer.has_handshaked:
                    peer.check_handshake()
                    continue

                if len(peer.buffer) < 4 or struct.unpack("!I", peer.buffer[:4])[0] == 0:  # keep alive
                    continue

                msg_length = utils.convert_bytes_to_decimal(peer.buffer[0:4])
                while len(peer.buffer) >= 4 + msg_length:
                    msg_code = int(ord(peer.buffer[4:5]))
                    payload = peer.buffer[5:4 + msg_length]
                    peer.buffer = peer.buffer[4 + msg_length:]
                    try:
                        peer.id_function[msg_code](payload)
                    except KeyError:
                        pass

    def request_stop(self):
        self.stop_requested = True

    def peers_bitfield(self, bitfield=None, peer=None, index=None):
        if index is not None:
            self.pieces_by_peer[index] = ["", []]
            return

        for i in range(len(self.pieces_by_peer)):
            if bitfield[i] == 1 and peer not in self.pieces_by_peer[i][1] and not self.pieces_by_peer[i][0] == "":
                self.pieces_by_peer[i][1].append(peer)
                self.pieces_by_peer[i][0] = len(self.pieces_by_peer[i][1])

    def get_unchoked_peer(self, index):
        for peer in self.peers:
            if peer.bitfield[index] and not peer.state["peer_choking"]:
                return peer
        return False

    def start_connection_to_peers(self):
        peers_to_handshake = [peer for peer in self.peers if not peer.has_handshaked and peer.last_handshake_attempt < time.time() - 10]
        for peer in peers_to_handshake:
            peer.last_handshake_attempt = time.time()
            try:
                peer.handshake()
                interested = peer.build_interested()
                peer.send(interested)
            except Exception as e:
                logging.error(peer.ip + ": removing peer because of: " + str(e))
                self.remove_peer(peer)

    def add_peer(self, peer):
        self.peers.append(peer)

    def remove_peer(self, peer):
        if peer in self.peers:
            try:
                peer.socket.close()
            except Exception:
                pass
            self.peers.remove(peer)

        for rarestPiece in self.rarestPieces.rarestPieces:
            if peer in rarestPiece["peers"]:
                rarestPiece["peers"].remove(peer)

    def get_peer_by_socket(self, socket):
        for peer in self.peers:
            if socket == peer.socket:
                return peer
        raise ("peer not present in PeerList")

    def request_new_piece(self, peer, index, offset, length):
        request = peer.build_request(index, offset, length)
        peer.send(request)

    def make_requests(self):
        max_requests = 50
        requests = 0
        i = 0
        if not self.peers:
            return
        pieces_by_file = self.piece_manager.pieces_by_file()
        pieces = [pieces for _, pieces in pieces_by_file for pieces in pieces]
        while i < len(pieces) and requests < max_requests:
            piece = pieces[i]
            peer = self.get_unchoked_peer(piece.index)
            if not peer:
                i += 1
                continue
            for idx, block in enumerate(piece.blocks):
                if block.status == "Free" or block.status == "Partial":
                    block.set_pending()
                    self.request_new_piece(peer, piece.index, idx * piece.BLOCK_SIZE, block.size)
                    requests += 1
            i += 1

    def enqueue_http_requests(self):
        i = 0
        if not self.request_queue.empty() or not self.http_peers:
            return
        pieces_by_file = self.piece_manager.pieces_by_file()
        while pieces_by_file:
            filename, pieces_containing_file = pieces_by_file.pop()
            for pieces in grouper(pieces_containing_file):
                self.piece_manager.set_pending(filename, pieces)
                for peer in self.http_peers:
                    if filename not in peer.fail_files:
                        self.request_queue.put((peer, filename, pieces), False)
                        i += 1
                        break

def grouper(pieces):
    resp = []
    length = 0
    temp_pieces = []
    for piece in pieces:
        temp_pieces.append(piece)
        if length > 5000000:
            resp.append(temp_pieces)
            temp_pieces = []
        length += piece.size
    resp.append(temp_pieces)

    # now we have a list of piece lists
    for idx, pieces in enumerate(resp):
        resp[idx] = [piece for piece in pieces if piece]
    resp = resp if resp[0] else []
    return resp
