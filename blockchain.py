#  Initializing the blockchain
blockchain = []


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    """ Append a new value as well as the last blockchain value to the blockchain

    Arguments:
        :transaction_amount: The amount that should be added.
        :last_transaction: The last blockchain transaction (default [1])
    """
    blockchain.append([last_transaction, transaction_amount])


def get_user_input():
    return float(input("Enter your transaction amount: "))


continue_loop = True

while continue_loop:
    print('1. Add block')
    print('2. Print blockchain')
    print('3. Exit')

    choice = int(input('Enter your choice: '))

    if choice == 1:
        value = get_user_input()
        if len(blockchain) == 0:
            add_value(value)
        else:
            add_value(transaction_amount=value, last_transaction=get_last_blockchain_value())  # named parameters
    elif choice == 2:
        for block in blockchain:
            print('Block: ' + str(block))
            # print(block)
    elif choice == 3:
        continue_loop = False
    else:
        print('Invalid choice. Please enter 1 - 3')

