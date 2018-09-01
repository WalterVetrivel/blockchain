import functools
import json

import hash_util
from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10  # constant with reward for miners

#  Initializing the blockchain
blockchain = []
open_transactions = []
owner = 'Walter'


def initialize_blockchain():
    global genesis_block
    global blockchain
    global open_transactions

    genesis_block = Block(0, '', [], 100, 0)
    blockchain = [genesis_block]

    open_transactions = []


def load_data():
    try:
        with open('blockchain.txt', mode='r') as f:
            file_content = f.readlines()
            global blockchain
            global open_transactions
            blockchain = json.loads(file_content[0][:-1])  # the :-1 is used to exclude the \n character at the end
            # We need to convert the transactions & open transactions to OrderedDict to get correct hash values

            updated_blockchain = []
            for block in blockchain:
                transactions = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                updated_block = Block(block['index'], block['previous_hash'], transactions, block['proof'], block['timestamp'])
                updated_blockchain.append(updated_block)

            blockchain = updated_blockchain

            open_transactions = json.loads(file_content[1])
            open_transactions = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in open_transactions]
    except (IOError, IndexError):
        initialize_blockchain()


load_data()


def save_data():
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
                               for block_el in blockchain]]
            f.write(json.dumps(saveable_chain))
            f.write('\n')
            saveable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_tx))
    except IOError:
        print('Unable to save')


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def get_balance(participant):
    """ Returns the balance of the participant (difference between total amount received and total amount sent)
    Open transactions are checked only for amount sent.
    Arguments:
         :participant: The participant whose balance needs to be checked
    """
    # List comprehension with if
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)

    amount_sent = functools.reduce(
        lambda tx_sum, tx_amount: tx_sum + (sum(tx_amount) if len(tx_amount) > 0 else 0), tx_sender, 0
    )  # sum returns sum of all values in the list

    tx_recipient = [[tx.amount for tx in block.transactions
                     if tx.recipient == participant]
                    for block in blockchain]

    amount_received = functools.reduce(
        lambda tx_sum, tx_amount: tx_sum + (sum(tx_amount) if len(tx_amount) > 0 else 0), tx_recipient, 0
    )

    return amount_received - amount_sent


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value as well as the last blockchain value to the blockchain

    Arguments:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :amount: The amount of coins sent with the transaction (default=1.0)
    """
    # we are using OrderedDict to get an ordered dictionary so that the hash doesn't change due to the order changing
    transaction = Transaction(sender, recipient, amount)

    verifier = Verification()
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        save_data()
        return True
    return False


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_util.hash_block(last_block)
    proof = 0
    verifier = Verification()
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def mine_block():
    """ Adds a new block to the blockchain. All open transactions are added to the block.
    A reward is given to the miner who mines a block.
    Returns True if successful, and this is used to close all open transactions."""

    last_block = blockchain[-1]
    hashed_block = hash_util.hash_block(last_block)

    proof = proof_of_work()

    # we are using OrderedDict to get an ordered dictionary so that the hash doesn't change due to the order changing
    reward_transaction = Transaction('MINING', owner, MINING_REWARD)
    copied_transactions = open_transactions[:]  # copies open_transactions by value (: signifies range, if nothing is
    # specified, then the whole list is copied
    copied_transactions.append(reward_transaction)  # reward for miners

    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True


def get_transaction_value():
    tx_recipient = input('Enter the recipient: ')
    tx_amount = float(input('Enter the transaction amount: '))
    return tx_recipient, tx_amount


def get_user_input():
    return int(input('Enter your choice: '))


def print_blockchain():
    for block in blockchain:
        print('Block: ' + str(block))


continue_loop = True

while continue_loop:
    print('1. Add new transaction')
    print('2. Mine new block')
    print('3. Print blockchain')
    print('4. Check transactions')
    print('0. Exit')

    choice = get_user_input()
    verifier = Verification()

    if choice == 1:
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient=recipient, amount=amount):
            print('Added transaction.')
        else:
            print('Transaction failed.')
        print(open_transactions)
    elif choice == 2:
        if mine_block():
            open_transactions = []
            save_data()
    elif choice == 3:
        print_blockchain()
    elif choice == 4:
        if verifier.check_transactions(open_transactions, get_balance):
            print('All transactions are valid.')
        else:
            print('There are invalid transactions.')
    elif choice == 0:
        continue_loop = False
    else:
        print('Invalid choice. Please enter 1 - 3')

    if not verifier.verify_chain(blockchain):
        print('Chain is invalid')
        break

    # print('Balance: ' + str(get_balance(owner)))
    print('Balance of {} is {:6.2f}'.format(owner, get_balance(owner)))
else:
    print('Goodbye')
