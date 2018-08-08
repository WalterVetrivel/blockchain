#  Initializing the blockchain
genesis_block = {
        'previous_hash': '',
        'index': 0,
        'transactions': []
    }
blockchain = [genesis_block]
open_transactions = []
owner = 'Walter'

def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


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

    open_transactions.append(transaction)


def hash_block(block):
    hashed_block = ''
    for key in block:
        value = block[key]
        hashed_block = hashed_block + str(value)
    return hashed_block


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
    }

    blockchain.append(block)


def get_transaction_value():
    tx_recipient = input('Enter the recipient: ')
    tx_amount = float(input('Enter the transaction amount: '))
    return tx_recipient, tx_amount


def verify_chain():
    is_valid = True

    for block_index in range(1, len(blockchain)):
        if blockchain[block_index]['previous_hash'] != hash_block(blockchain[block_index - 1]):
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
    print('4. Manipulate chain')
    print('0. Exit')

    choice = int(input('Enter your choice: '))

    if choice == 1:
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(recipient=recipient, amount=amount)
        print(open_transactions)
    elif choice == 2:
        mine_block()
    elif choice == 3:
        print_blockchain()
    elif choice == 4:
        if len(blockchain) > 0:
            blockchain[0]['amount'] = 50
    elif choice == 0:
        continue_loop = False
    else:
        print('Invalid choice. Please enter 1 - 3')

    if not verify_chain():
        print('Chain is invalid')
        break

