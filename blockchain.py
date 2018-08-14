import functools
from collections import OrderedDict
import json

import hash_util

MINING_REWARD = 10  # constant with reward for miners

#  Initializing the blockchain
genesis_block = {
        'previous_hash': '',
        'index': 0,
        'transactions': [],
        'proof': 100
    }
blockchain = [genesis_block]

open_transactions = []
owner = 'Walter'
participants = {'Walter'}


def load_data():
    with open('blockchain.txt', mode='r') as f:
        file_content = f.readlines()
        global blockchain
        global open_transactions
        blockchain = json.loads(file_content[0][:-1])  # the :-1 is used to exclude the \n character at the end
        # We need to convert the transactions & open transactions to OrderedDict to get correct hash values
        blockchain = [
            {
                'previous_hash': block['previous_hash'],
                'index': block['index'],
                'proof': block['proof'],
                'transactions': [OrderedDict([('sender', tx['sender']),
                                              ('recipient', tx['recipient']),
                                              ('amount', tx['amount'])])
                                 for tx in block['transactions']]
            } for block in blockchain]
        open_transactions = json.loads(file_content[1])
        open_transactions = [OrderedDict([('sender', tx['sender']),
                                          ('recipient', tx['recipient']),
                                          ('amount', tx['amount'])])
                             for tx in open_transactions]


load_data()


def save_data():
    with open('blockchain.txt', mode='w') as f:
        f.write(json.dumps(blockchain))
        f.write('\n')
        f.write(json.dumps(open_transactions))


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
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)

    amount_sent = functools.reduce(
        lambda tx_sum, tx_amount: tx_sum + (sum(tx_amount) if len(tx_amount) > 0 else 0), tx_sender, 0
    )  # sum returns sum of all values in the list

    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant]
                    for block in blockchain]

    amount_received = functools.reduce(
        lambda tx_sum, tx_amount: tx_sum + (sum(tx_amount) if len(tx_amount) > 0 else 0), tx_recipient, 0
    )

    return amount_received - amount_sent


def verify_transaction(transaction):
    """ Check whether the sender has enough balance to send the the amount.
    Arguments:
        :transaction: The transaction that must be verified
    """

    sender_balance = get_balance(transaction['sender'])
    if sender_balance >= transaction['amount']:
        return True
    return False


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value as well as the last blockchain value to the blockchain

    Arguments:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :amount: The amount of coins sent with the transaction (default=1.0)
    """
    # we are using OrderedDict to get an ordered dictionary so that the hash doesn't change due to the order changing
    transaction = OrderedDict([('sender', sender), ('recipient', recipient), ('amount', amount)])

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_util.hash_string_256(guess)
    return guess_hash[0:2] == '00'  # If generated hash has two leading 0's, it is valid. The condition can be changed.


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_util.hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def check_transactions():
    return all([verify_transaction(transaction) for transaction in open_transactions])


def mine_block():
    """ Adds a new block to the blockchain. All open transactions are added to the block.
    A reward is given to the miner who mines a block.
    Returns True if successful, and this is used to close all open transactions."""

    last_block = blockchain[-1]
    hashed_block = hash_util.hash_block(last_block)

    proof = proof_of_work()

    # we are using OrderedDict to get an ordered dictionary so that the hash doesn't change due to the order changing
    reward_transaction = OrderedDict([('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])

    # copied_transactions = [transaction for transaction in open_transactions]
    copied_transactions = open_transactions[:]  # copies open_transactions by value (: signifies range, if nothing is
    # specified, then the whole list is copied
    copied_transactions.append(reward_transaction)  # reward for miners
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }

    blockchain.append(block)
    return True


def get_transaction_value():
    tx_recipient = input('Enter the recipient: ')
    tx_amount = float(input('Enter the transaction amount: '))
    return tx_recipient, tx_amount


def verify_chain():
    is_valid = True

    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_util.hash_block(blockchain[index - 1]):
            is_valid = False
            break
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            is_valid = False
            break

    return is_valid


def print_blockchain():
    for block in blockchain:
        print('Block: ' + str(block))


continue_loop = True

while continue_loop:
    print('1. Add new transaction')
    print('2. Mine new block')
    print('3. Print blockchain')
    print('4. Show participants')
    print('5. Check transactions')
    print('100. Manipulate chain')
    print('0. Exit')

    choice = int(input('Enter your choice: '))

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
        print(participants)
    elif choice == 5:
        if check_transactions():
            print('All transactions are valid.')
        else:
            print('There are invalid transactions.')
    elif choice == 100:
        if len(blockchain) > 0:
            blockchain[0]['amount'] = 50
    elif choice == 0:
        continue_loop = False
    else:
        print('Invalid choice. Please enter 1 - 3')

    if not verify_chain():
        print('Chain is invalid')
        break

    # print('Balance: ' + str(get_balance(owner)))
    print('Balance of {} is {:6.2f}'.format(owner, get_balance(owner)))
else:
    print('Goodbye')
