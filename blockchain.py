import functools

MINING_REWARD = 10  # constant with reward for miners

#  Initializing the blockchain
genesis_block = {
        'previous_hash': '',
        'index': 0,
        'transactions': []
    }
blockchain = [genesis_block]

open_transactions = []
owner = 'Walter'
participants = {'Walter'}


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
        lambda tx_sum, tx_amount: tx_sum + (tx_amount[0] if len(tx_amount) > 0 else 0), tx_sender, 0
    )

    # amount_sent = 0
    # for tx in tx_sender:
    #     for amount in tx:
    #         amount_sent += amount

    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant]
                    for block in blockchain]

    amount_received = functools.reduce(
        lambda tx_sum, tx_amount: tx_sum + (tx_amount[0] if len(tx_amount) > 0 else 0), tx_recipient, 0
    )
    # amount_received = 0
    # for tx in tx_recipient:
    #     for amount in tx:
    #         amount_received += amount

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
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def hash_block(block):
    hashed_block = '-'.join([str(block[key]) for key in block])  # List comprehension
    return hashed_block


def check_transactions():
    return all([verify_transaction(transaction) for transaction in open_transactions])


def mine_block():
    """ Adds a new block to the blockchain. All open transactions are added to the block.
    A reward is given to the miner who mines a block.
    Returns True if successful, and this is used to close all open transactions."""

    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    # copied_transactions = [transaction for transaction in open_transactions]
    copied_transactions = open_transactions[:]  # copies open_transactions by value (: signifies range, if nothing is
    # specified, then the whole list is copied
    copied_transactions.append(reward_transaction)  # reward for miners
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions
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
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
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
