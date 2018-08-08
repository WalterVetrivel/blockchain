#  Initializing the blockchain
blockchain = []


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(transaction_amount, last_transaction):
    """ Append a new value as well as the last blockchain value to the blockchain

    Arguments:
        :transaction_amount: The amount that should be added.
        :last_transaction: The last blockchain transaction (default [1])
    """
    if last_transaction is None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_transaction_value():
    return float(input("Enter your transaction amount: "))


def verify_chain():
    is_valid = True

    for block_index in range(1, len(blockchain), 1):
        if blockchain[block_index][0] != blockchain[block_index - 1]:
            is_valid = False
            break

    return is_valid


continue_loop = True

while continue_loop:
    print('1. Add block')
    print('2. Print blockchain')
    print('3. Manipulate chain')
    print('0. Exit')

    choice = int(input('Enter your choice: '))

    if choice == 1:
        value = get_transaction_value()
        add_transaction(transaction_amount=value, last_transaction=get_last_blockchain_value())  # named parameters
    elif choice == 2:
        for block in blockchain:
            print('Block: ' + str(block))
    elif choice == 3:
        if len(blockchain) > 0:
            blockchain[0] = [2]
    elif choice == 0:
        continue_loop = False
    else:
        print('Invalid choice. Please enter 1 - 3')

    if not verify_chain():
        print('Chain is invalid')
        break

