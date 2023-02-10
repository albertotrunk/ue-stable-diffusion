import logging
import json
import os
from .PieceManager import PieceManager
from .Torrent import Torrent
from .Client import Client
from .utils import read_timestamp, timestamp_is_within_30_days, filenames_present, write_timestamp, clean_path


def get(at_hash, datastore="", urls=[], showlogs=False, use_timestamp=True):
    logging.getLogger().setLevel(logging.CRITICAL)

    if showlogs:
        logging.getLogger().setLevel(level=logging.INFO)

    if not datastore:
        datastore = "~/.academictorrents-datastore"

    torrent = Torrent(at_hash, datastore)
    torrent.urls = torrent.urls + urls
    path = torrent.datastore + torrent.contents['info']['name']

    # Check timestamp
    timestamp = read_timestamp(at_hash)
    if timestamp_is_within_30_days(timestamp) and filenames_present(torrent) and use_timestamp:
        print("File verified recently. Assumed still correct. Set use_timestamp=False to check again.")
        return path

    # Check if downloaded and finished
    piece_manager = PieceManager(torrent)
    piece_manager.check_disk_pieces()
    downloaded_amount = piece_manager.check_finished_pieces()
    if float(downloaded_amount) / torrent.total_length == 1.0:
        print("Found dataset at " + path)
    else:
        print("Downloading to " + path)
        Client(torrent, downloaded_amount, piece_manager).start()

    if use_timestamp:
        write_timestamp(at_hash)
    return path

def set_datastore(datastore, path_to_config_file="~/.academictorrents.config"):
    json.dump({"datastore": datastore}, open(clean_path(path_to_config_file), "w+"))
