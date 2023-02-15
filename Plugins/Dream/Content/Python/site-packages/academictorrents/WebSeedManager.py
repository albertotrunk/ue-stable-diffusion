from threading import Thread
import urllib3
from queue import Queue
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebSeedManager(Thread):
    def __init__(self, request_queue, http_peers):
        Thread.__init__(self)
        self.request_queue = request_queue
        self.stop_requested = False
        self.http_peers = http_peers

    def run(self):
        while not self.stop_requested:
            try:
                httpPeer, filename, pieces = self.request_queue.get(timeout=1)
            except Exception:
                continue
            if not pieces:
                self.request_queue.task_done()
                continue
            response = httpPeer.request_ranges(filename, pieces)
            if not response or response.status_code != 206:
                httpPeer.fail_files.append(filename)
                for http_peer in self.http_peers:
                    response = http_peer.request_ranges(filename, pieces)
                    if response and response.status_code == 206:
                        httpPeer.publish_responses(response, filename, pieces)
                        break
                self.request_queue.task_done()
                continue
            httpPeer.publish_responses(response, filename, pieces)
            self.request_queue.task_done()

    def request_stop(self):
        self.stop_requested = True
