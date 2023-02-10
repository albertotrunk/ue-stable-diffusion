import time
import bencode
import logging
import os
import requests
from . import utils
try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError


class Torrent(object):
    def __init__(self, hash, datastore):
        self.hash = hash
        self.datastore = utils.get_datastore(datastore=datastore)
        contents = ""
        if not os.path.isdir(self.datastore):
            os.makedirs(self.datastore)
        try:
            contents = open("/tmp/" + hash + '.torrent', 'rb').read()
        except Exception:
            contents = self.get_from_file()
            if not contents:
                contents = self.get_from_url()
            if not contents:
                raise Exception("Could not find a torrent with this hash on the tracker or in the data directory:" + str(self.datastore))

        self.contents = bencode.decode(contents)
        self.total_length = 0
        self.piece_length = self.contents['info']['piece length']
        self.pieces = self.contents['info']['pieces']

        self.info_hash = utils.sha1_hash(bencode.encode(self.contents['info']))
        self.peer_id = self.generate_peer_id()
        self.trackers = self.get_trackers()
        self.urls = self.get_urls()
        self.filenames = []

        self.get_files()
        if self.total_length % self.piece_length == 0:
            self.number_of_pieces = self.total_length / self.piece_length
        else:
            self.number_of_pieces = int(self.total_length / self.piece_length) + 1

        logging.debug(self.trackers)
        logging.debug(self.filenames)

        assert(self.total_length > 0)
        assert(len(self.filenames) > 0)

        name = self.contents['info']['name']
        if "length" in self.contents['info']:
            size_mb = self.contents['info']['length']/1000./1000.
        else:
            total_length = 0
            for f in self.contents['info']['files']:
                total_length += f['length']
            size_mb = total_length/1000./1000.

        print("Torrent name: " + name + ", Size: {0:.2f}MB".format(size_mb))

    def get_urls(self):
        urls = []
        for url in self.contents.get('url-list'):
            if not url:
                continue
            try:
                resp = requests.head(url)
                if resp.headers.get('Accept-Ranges', False):
                    urls.append('/'.join(url.split('/')[0:-1]) + '/')
                    continue
            except Exception as e:
                continue
            directory = self.contents.get('info', {}).get('name')
            filename = self.contents.get('info', {}).get('files', [{'path': ['']}])[0].get('path')[0]
            if url[-1] == '/':
                url = url + directory + '/'
            else:
                url = url + '/' + directory + '/'

            resp = requests.head(url + filename)
            if resp.headers.get('Accept-Ranges', False):
                urls.append(url)
        return urls

    def get_from_file(self):
        torrent_path = os.path.join("/tmp/", self.hash + '.torrent')
        try:
            return open(torrent_path, 'rb').read()
        except Exception:
            return None
        return

    def get_from_url(self):
        contents = None
        url = "http://academictorrents.com/download/" + self.hash
        torrent_path = os.path.join("/tmp/", self.hash + '.torrent')
        response = urlopen(url, timeout=5).read()
        open(torrent_path, 'wb').write(response)
        try:
            return open(torrent_path, 'rb').read()
        except Exception:
            return None

    def get_files(self):
        root = self.datastore + self.contents['info']['name']
        if 'files' in self.contents['info']:
            if not os.path.exists(root):
                os.mkdir(root, 0o766)

            for f in self.contents['info']['files']:
                path = os.path.join(root, *f["path"])

                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))

                self.filenames.append({"path": path, "length": f["length"]})
                self.total_length += f["length"]
        else:
            self.filenames.append({"path": root, "length": self.contents['info']['length']})
            self.total_length = self.contents['info']['length']

    def get_trackers(self):
        if 'announce-list' in self.contents:
            return self.contents['announce-list']
        else:
            return [[self.contents['announce']]]

    def generate_peer_id(self):
        seed = str(time.time())
        return utils.sha1_hash(seed.encode())
