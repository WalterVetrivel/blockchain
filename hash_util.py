import hashlib
import json


def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    # hashlib.sha256() returns a byte hash that needs to be converted to printable characters using hexdigest()
    # json.dumps(block).encode() converts block to string
    # sort_keys=True is needed because dictionaries are unordered and if order changes, hash changes

    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
