import hashlib
import json


def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    # hashlib.sha256() returns a byte hash that needs to be converted to printable characters using hexdigest()
    # json.dumps(block).encode() converts block to string
    # sort_keys=True is needed because dictionaries are unordered and if order changes, hash changes
    return hash_string_256(json.dumps(block, sort_keys=True).encode())
