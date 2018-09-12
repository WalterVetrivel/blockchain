from uuid import uuid4

from verification import Verification
from blockchain import Blockchain

class Node:
    def __init__(self):
        # self.node_id = str(uuid4())
        self.node_id = 'Walter'
        self.blockchain = Blockchain(self.node_id)

    def get_transaction_value(self):
        tx_recipient = input('Enter the recipient: ')
        tx_amount = float(input('Enter the transaction amount: '))
        return tx_recipient, tx_amount

    def get_user_input(self):
        return int(input('Enter your choice: '))

    def print_blockchain(self):
        for block in self.blockchain.chain:
            print('Block: ' + str(block))

    def listen_for_input(self):
        continue_loop = True

        while continue_loop:
            print('1. Add new transaction')
            print('2. Mine new block')
            print('3. Print blockchain')
            print('4. Check transactions')
            print('0. Exit')

            choice = self.get_user_input()

            if choice == 1:
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient=recipient, sender=self.node_id, amount=amount):
                    print('Added transaction.')
                else:
                    print('Transaction failed.')
                print(self.blockchain.get_open_transactions())
            elif choice == 2:
                if self.blockchain.mine_block():
                    self.blockchain.save_data()
            elif choice == 3:
                self.print_blockchain()
            elif choice == 4:
                if Verification.check_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions are valid.')
                else:
                    print('There are invalid transactions.')
            elif choice == 0:
                continue_loop = False
            else:
                print('Invalid choice. Please enter 1 - 3')

            if not Verification.verify_chain(self.blockchain.chain):
                print('Chain is invalid')
                break

            print('Balance of {} is {:6.2f}'.format(self.node_id, self.blockchain.get_balance(self.node_id)))
        else:
            print('Goodbye')


node = Node()
node.listen_for_input()
