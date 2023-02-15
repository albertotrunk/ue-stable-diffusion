import sys
import time
import socket
import logging
import struct
import bitstring
from bitstring import BitArray
from pubsub import pub
from . import utils


class Peer(object):
    def __init__(self, torrent, ip, port=6881):
        self.last_handshake_attempt = 0
        self.has_handshaked = False
        self.counter = 10
        self.socket = None
        self.ip = ip
        self.port = port
        self.torrent = torrent
        self.socketsPeers = []
        self.buffer = bytearray(b"")

        self.state = {
            'am_choking': True,
            'am_interested': False,
            'peer_choking': True,
            'peer_interested': False,
        }

        self.id_function = {
            0: self.choke,
            1: self.unchoke,
            2: self.interested,
            3: self.not_interested,
            4: self.have,
            5: self.update_bitfield,
            6: self.request,
            7: self.piece,
            8: self.cancel,
            9: self.portRequest
        }

        self.number_of_pieces = torrent.number_of_pieces
        self.bitfield = bitstring.BitArray(self.number_of_pieces)

    def send(self, msg):
        try:
            self.socket.send(msg)
        except Exception as e:
            logging.error(str(self.ip) + ": send Error: " + str(e))

    def handshake(self):
        hs = self.build_handshake()
        self.send(hs)

    def check_handshake(self):
        if self.buffer[1:20] == b"BitTorrent protocol":
            handshake = self.buffer[:68]
            expected_length, info_dict, info_hash, peer_id = struct.unpack(
                "B" + str(len(b"BitTorrent protocol")) + "s8x20s20s",
                handshake)

            if self.torrent.info_hash == info_hash:
                self.has_handshaked = True
            else:
                logging.warning("Error with peer's handshake")

            self.buffer = self.buffer[28 + len(info_hash) + 20:]

    def connect(self, timeout=10):
        if self.socket:
            return True
        try:
            self.socket = socket.create_connection((self.ip, self.port), timeout)
            logging.info("connected to peer ip: {0} - port: {1}".format(self.ip, self.port))
            return True
        except Exception as e:
            logging.error(str(self.ip) + ": connect Socket Timeout Error")
        return False

    def build_handshake(self):
        pstr = "BitTorrent protocol".encode('utf-8')
        hs = struct.pack("B" + str(len(pstr)) + "s8x20s20s",
                         len(pstr),
                         pstr,
                         self.torrent.info_hash,
                         self.torrent.peer_id
                         )
        assert len(hs) == 49 + len(pstr)
        return hs

    def build_interested(self):
        return struct.pack('!I', 1) + struct.pack('!B', 2)

    def build_request(self, index, offset, length):
        header = struct.pack('>I', 13)
        id = b'\x06'

        if isinstance(length, (bytes, bytearray)):
            id = '\x06'

        index = struct.pack('>I', index)
        offset = struct.pack('>I', offset)
        length = struct.pack('>I', length)
        request = header + id + index + offset + length
        return request

    def build_piece(self, index, offset, data):
        header = struct.pack('>I', 13)
        id = '\x07'
        index = struct.pack('>I', index)
        offset = struct.pack('>I', offset)
        data = struct.pack('>I', data)
        piece = header + id + index + offset + data
        return piece

    def build_bitfield(self):
        length = struct.pack('>I', 4)
        id = '\x05'
        bitfield = self.bitfield.tobytes()
        bitfield = length + id + bitfield
        return bitfield

    def interested(self, payload=None):
        logging.info('interested')
        self.state['peer_interested'] = True

    def not_interested(self, payload=None):
        logging.info('not_interested')
        self.state['peer_interested'] = False

    def have(self, payload):
        index = utils.convert_bytes_to_decimal(payload)
        try:
            self.bitfield[index] = True
        except IndexError:
            pass
        pub.sendMessage('RarestPiece.update_peers_bitfield', bitfield=self.bitfield, peer=self)

    def update_bitfield(self, payload):
        self.bitfield = BitArray(bytes=payload)
        logging.info('request')
        pub.sendMessage('RarestPiece.update_peers_bitfield', bitfield=self.bitfield, peer=self)

    def request(self, payload):
        piece_index = payload[:4]
        block_offset = payload[4:8]
        block_length = payload[8:]
        logging.info('request')
        pub.sendMessage('PieceManager.PeerRequestsPiece', piece=(piece_index, block_offset, block_length), peer=self)

    def piece(self, payload):
        piece_index = utils.convert_bytes_to_decimal(payload[:4])
        piece_offset = utils.convert_bytes_to_decimal(payload[4:8])
        piece_data = payload[8:]
        pub.sendMessage('PieceManager.receive_block', piece=(piece_index, piece_offset, piece_data))

    def cancel(self, payload=None):
        logging.info('cancel')

    def portRequest(self, payload=None):
        logging.info('portRequest')

    def choke(self,payload=None):
        logging.info("choking peer: " + str(self.ip))
        self.state['peer_choking'] = True

    def unchoke(self,payload=None):
        logging.info("Unchoking peer: " + str(self.ip))
        self.state['peer_choking'] = False
