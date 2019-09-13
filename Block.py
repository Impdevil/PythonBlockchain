from hashlib import sha512
import json
import time


class Block:
    """Block for blockchain python """

    def __init__(self, index, vote_data, timestamp, PREV_hash):
        self.index = index
        self.voteData = vote_data

        self.timestamp = timestamp
        self.Previous_Hash = PREV_hash


    def Compute_Hash(self):
        """ a function that creates the hash of a block"""
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha512(block_string.encode()).hexdigest()


class VoteData():
    IDhash = ""
    name =""

