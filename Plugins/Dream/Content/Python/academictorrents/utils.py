import hashlib
import os
import json
import datetime
import calendar
import time


def convert_bytes_to_decimal(headerBytes):
    size = 0
    power = len(headerBytes) - 1
    for ch in headerBytes:
        if isinstance(ch, int):
            size += ch * 256 ** power
        else:
            size += int(ord(ch)) * 256 ** power
        power -= 1
    return size


def sha1_hash(string):
    """Return 20-byte sha1 hash of string."""
    return hashlib.sha1(string).digest()


def get_timestamp_filename():
    return clean_path("~/.academictorrents_timestamps.json")


def get_datastore(datastore="", path_to_config_file="~/.academictorrents.config"):
    if datastore:
        datastore = clean_path(datastore)
    else:
        datastore = json.loads(open(clean_path(path_to_config_file)).read()).get("datastore", os.getcwd() + "/datastore/")
    if datastore[-1] != "/":
        datastore = datastore + "/"
    return datastore

def clean_path(path=None):
    if path.startswith("~"):
        return os.path.expanduser(path)
    else:
        return os.path.abspath(path)

def write_timestamp(at_hash):
    filename = get_timestamp_filename()
    try:
        f = open(filename, 'r')
        timestamps = json.load(f)
        f.close()
    except Exception:
        timestamps = {}
    timestamps[at_hash] = int(datetime.datetime.now().strftime("%s"))
    f = open(filename, 'w')
    json.dump(timestamps, f)

def read_timestamp(at_hash):
    filename = get_timestamp_filename()
    try:
        f = open(filename, 'r')
        timestamp = json.load(f).get(at_hash, 0)
        f.close()
    except Exception:
        timestamp = 0
    return timestamp


def timestamp_is_within_30_days(timestamp):
    seconds_in_a_month = 86400 * 30
    if timestamp > int(calendar.timegm(time.gmtime())) - seconds_in_a_month:
        return True
    return False


def timestamp_is_within_10_seconds(timestamp):
    ten_seconds = 10
    if timestamp > int(calendar.timegm(time.gmtime())) - ten_seconds:
        return True
    return False


def filenames_present(torrent):
    return torrent.contents['info']['name'] in os.listdir(torrent.datastore)
