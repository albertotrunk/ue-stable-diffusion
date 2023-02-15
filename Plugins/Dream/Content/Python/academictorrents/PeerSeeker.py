import time
from queue import Queue
from . import Peer
from threading import Thread
from pubsub import pub


class PeerSeeker(Thread):
    def __init__(self, new_peers_queue, torrent, peer_manager):
        Thread.__init__(self)
        self.stop_requested = False
        self.peer_manager = peer_manager
        self.new_peers_queue = new_peers_queue
        self.torrent = torrent
        self.reset_time = time.time()

    def request_stop(self):
        self.stop_requested = True

    def run(self):
        failed_peers = []
        while not self.stop_requested:
            # reset failed peers so we can try again
            if (time.time() - self.reset_time) > 10:
                failed_peers = []
                self.reset_time = time.time()
            try:
                peer = self.new_peers_queue.get(timeout=1)
            except Exception:
                continue
            peer = Peer.Peer(self.torrent, peer[0], peer[1])
            extant_peers = [(peer.ip, peer.port) for peer in self.peer_manager.peers]
            if (peer.ip, peer.port) in failed_peers or (peer.ip, peer.port) in extant_peers:
                continue

            if peer.connect(5):
                pub.sendMessage('PeerManager.new_peer', peer=peer)
            else:
                failed_peers.append((peer.ip, peer.port))
