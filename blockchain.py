import functools
import json

import hash_util
from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10  # constant with reward for miners


class Blockchain:
    def __init__(self, hosting_node_id):
        #  Initializing the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        self.__chain = [genesis_block]
        self.__open_transactions = []
        self.hosting_node = hosting_node_id
        self.load_data()

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transaction(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                blockchain = json.loads(file_content[0][:-1])  # the :-1 is used to exclude the \n character at the end
                # We need to convert the transactions & open transactions to OrderedDict to get correct hash values

                updated_blockchain = []
                for block in blockchain:
                    transactions = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in
                                    block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], transactions, block['proof'],
                                          block['timestamp'])
                    updated_blockchain.append(updated_block)

                self.__chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                self.__open_transactions = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in
                                          open_transactions]
        except (IOError, IndexError):
            pass

    def save_data(self):
        try:
            with open('blockchain.txt', mode='w') as f:
                saveable_chain = [block.__dict__
                                  for block in
                                  [Block
                                   (block_el.index,
                                    block_el.previous_hash,
                                    [tx.__dict__ for tx in block_el.transactions],
                                    block_el.proof,
                                    block_el.timestamp)
                                   for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
        except IOError:
            print('Unable to save')

    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_util.hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self, participant):
        """ Returns the balance of the participant (difference between total amount received and total amount sent)
        Open transactions are checked only for amount sent.
        Arguments:
             :participant: The participant whose balance needs to be checked
        """
        # List comprehension with if
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)

        amount_sent = functools.reduce(
            lambda tx_sum, tx_amount: tx_sum + (sum(tx_amount) if len(tx_amount) > 0 else 0), tx_sender, 0
        )  # sum returns sum of all values in the list

        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == participant]
                        for block in self.__chain]

        amount_received = functools.reduce(
            lambda tx_sum, tx_amount: tx_sum + (sum(tx_amount) if len(tx_amount) > 0 else 0), tx_recipient, 0
        )

        return amount_received - amount_sent

    def add_transaction(self, recipient, sender, amount=1.0):
        """ Append a new value as well as the last blockchain value to the blockchain

        Arguments:
            :sender: The sender of the coins.
            :recipient: The recipient of the coins.
            :amount: The amount of coins sent with the transaction (default=1.0)
        """
        # we are using OrderedDict to get an ordered dictionary so that the hash doesn't change due to the order changing
        transaction = Transaction(sender, recipient, amount)

        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        """ Adds a new block to the blockchain. All open transactions are added to the block.
        A reward is given to the miner who mines a block.
        Returns True if successful, and this is used to close all open transactions."""

        last_block = self.__chain[-1]
        hashed_block = hash_util.hash_block(last_block)

        proof = self.proof_of_work()

        # we are using OrderedDict to get an ordered dictionary so that the hash doesn't change due to the order changing
        reward_transaction = Transaction('MINING', self.hosting_node, MINING_REWARD)
        copied_transactions = self.__open_transactions[:]  # copies open_transactions by value (: signifies range, if nothing is
        # specified, then the whole list is copied
        copied_transactions.append(reward_transaction)  # reward for miners

        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transactions = []
        return True
