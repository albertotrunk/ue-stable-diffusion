import bencode
import requests
import logging
import struct
import random
import socket
import threading
import datetime
import time
from threading import Thread
from . import utils
from .version import __version__
# Python 2 and 3: alternative 4
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        threading.Thread.__init__(self)
        self._target = target
        self._args = args

    def run(self):
        self._target(*self._args)


class Tracker(Thread):
    def __init__(self, torrent, new_peers_queue, downloaded):
        Thread.__init__(self)
        self.torrent = torrent
        self.lstThreads = []
        self.new_peers_queue = new_peers_queue
        self.stop_requested = False
        self.downloaded = downloaded
        self.last_message_time = int(datetime.datetime.now().strftime("%s"))
        self.last_update_time = int(datetime.datetime.now().strftime("%s"))

    def request_stop(self):
        self.stop_requested = True

    def run(self):
        while not self.stop_requested:
            self.getPeersFromTrackers()
            time.sleep(10)
            self.downloading_message()
        self.stop_message()

    def getPeersFromTrackers(self):
        if utils.timestamp_is_within_10_seconds(self.last_update_time):
            return
        self.last_update_time = int(datetime.datetime.now().strftime("%s"))

        for tracker in self.torrent.trackers:
            if tracker[0] == '':
                continue
            elif tracker[0][:4] == "http":
                t1 = FuncThread(self.scrapeHTTP, self.torrent, tracker[0])
                self.lstThreads.append(t1)
                t1.start()
            else:
                t2 = FuncThread(self.scrape_udp, self.torrent, tracker[0])
                self.lstThreads.append(t2)
                t2.start()

        for t in self.lstThreads:
            t.join()

    def request_stop(self):
        self.stop_requested = True

    def set_downloaded(self, size):
        self.downloaded = size

    def scrapeHTTP(self, torrent, tracker):
        params = {
            'info_hash': torrent.info_hash,
            'peer_id': torrent.peer_id,
            'uploaded': 0,
            'downloaded': 0,
            'left': torrent.total_length,
            'event': 'started',
            'port': 6881
        }
        try:
            answerTracker = requests.get(tracker, params=params, timeout=30, headers={'user-agent': "AT-Client/" + __version__ + " " + requests.utils.default_user_agent()})
            lstPeers = bencode.decode(answerTracker.content)
            for peer in lstPeers['peers']:
                self.new_peers_queue.put([peer['ip'], peer['port']])
        except Exception as e:
            logging.info(e)
            pass

    def stop_message(self):
        resp = requests.models.Response()
        for tracker in self.torrent.trackers:
            if tracker[0] == '':
                continue
            elif tracker[0][:4] == "http":
                event = "completed" if self.torrent.total_length == self.downloaded else "stopped"
                params = {
                    'info_hash': self.torrent.info_hash,
                    'peer_id': self.torrent.peer_id,
                    'uploaded': 0,
                    'downloaded': self.downloaded,
                    'left': 0,
                    'event': event,
                    'port': 6881
                }
                try:
                    resp = requests.post(tracker[0], params=params, timeout=30, headers={'user-agent': "AT-Client/" + __version__ + " " + requests.utils.default_user_agent()})
                except Exception as e:
                    pass
            return params, resp

    def downloading_message(self):
        if utils.timestamp_is_within_10_seconds(self.last_message_time):
            return
        self.last_message_time = int(datetime.datetime.now().strftime("%s"))
        resp = requests.models.Response()
        if self.downloaded == 0:
            return True
        for tracker in self.torrent.trackers:
            if tracker[0] == '':
                continue
            elif tracker[0][:4] == "http":
                params = {
                    'info_hash': self.torrent.info_hash,
                    'peer_id': self.torrent.peer_id,
                    'uploaded': 0,
                    'downloaded': self.downloaded,
                    'left': self.torrent.total_length - self.downloaded,
                    'port': 6881
                }
                try:
                    resp = requests.get(tracker[0], params=params, timeout=30, headers={'user-agent': "AT-Client/" + __version__ + " " + requests.utils.default_user_agent()})
                except Exception as e:
                    logging.info(e)
                    pass
            return params, resp

    def make_connection_id_request(self):
        conn_id = struct.pack('>Q', 0x41727101980)
        action = struct.pack('>I', 0)
        trans_id = struct.pack('>I', random.randint(0, 100000))
        return (conn_id + action + trans_id, trans_id, action)

    def make_announce_input(self, info_hash, conn_id, peer_id):
        action = struct.pack('>I', 1)
        trans_id = struct.pack('>I', random.randint(0, 100000))

        downloaded = struct.pack('>Q', 0)
        left = struct.pack('>Q', 0)
        uploaded = struct.pack('>Q', 0)

        event = struct.pack('>I', 0)
        ip = struct.pack('>I', 0)
        key = struct.pack('>I', 0)
        num_want = struct.pack('>i', -1)
        port = struct.pack('>h', 8000)

        msg = (conn_id + action + trans_id + info_hash + peer_id + downloaded +
               left + uploaded + event + ip + key + num_want + port)

        return msg, trans_id, action

    def send_msg(self, conn, sock, msg, trans_id, action, size):
        sock.sendto(msg, conn)
        try:
            response = sock.recv(2048)
        except socket.timeout as err:
            logging.info(err)
            return
            # logging.debug("Connecting again...")
            # return self.send_msg(conn, sock, msg, trans_id, action, size)
        if len(response) < size:
            logging.debug("Did not get full message. Connecting again...")
            return self.send_msg(conn, sock, msg, trans_id, action, size)

        if action != response[0:4] or trans_id != response[4:8]:
            logging.debug("Transaction or Action ID did not match. Trying again...")
            return self.send_msg(conn, sock, msg, trans_id, action, size)

        return response

    def scrape_udp(self, torrent, announce):
        try:
            parsed = urlparse(announce)
            ip = socket.gethostbyname(parsed.hostname)

            if ip == '127.0.0.1':
                return False
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(30)
            conn = (ip, parsed.port)
            msg, trans_id, action = self.make_connection_id_request()
            response = self.send_msg(conn, sock, msg, trans_id, action, 16)
            if response is None:
                return ""

            conn_id = response[8:]
            msg, trans_id, action = self.make_announce_input(torrent.info_hash, conn_id, torrent.peer_id)
            response = self.send_msg(conn, sock, msg, trans_id, action, 20)
            if response is None or response is "":
                return ""
            peersByte = response[20:]
            raw_bytes = [ord(c) for c in peersByte]
            for i in range(len(raw_bytes) / 6):
                start = i * 6
                end = start + 6
                ip = ".".join(str(i) for i in raw_bytes[start:end - 2])
                port = raw_bytes[end - 2:end]
                port = port[1] + port[0] * 256
                self.new_peers_queue.put([ip, port])
        except Exception:
            pass
