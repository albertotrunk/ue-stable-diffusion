import requests
import math
from pubsub import pub
from threading import Thread
import urllib3
import logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HttpPeer(object):
    def __init__(self, url):
        self.url = url
        self.sess = requests.Session()
        self.fail_files = []

    def request_ranges(self, filename, pieces):
        start = pieces[0].get_file_offset(filename)
        end = start
        for piece in pieces:
            end += piece.get_length(filename)
        try:
            return self.sess.get(self.url + filename, headers={'Range': 'bytes=' + str(start) + '-' + str(end)}, verify=False, timeout=5)
        except Exception as e:
            logging.info(str(e))
            return False

    def publish_responses(self, response, filename, pieces):
        offset = 0
        for piece in pieces:
            size = piece.get_length(filename)
            pub.sendMessage('PieceManager.receive_file', piece=(piece.index, filename, response.content[offset: offset + size]))
            offset += size
