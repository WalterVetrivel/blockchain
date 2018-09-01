import hash_util


class Verification:
    def valid_proof(self, transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_util.hash_string_256(guess)
        return guess_hash[
               0:2] == '00'  # If generated hash has two leading 0's, it is valid. The condition can be changed.

    def verify_chain(self, blockchain):
        is_valid = True

        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_util.hash_block(blockchain[index - 1]):
                is_valid = False
                break
            if not self.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                is_valid = False
                break

        return is_valid

    def verify_transaction(self, transaction, get_balance):
        """ Check whether the sender has enough balance to send the the amount.
        Arguments:
            :transaction: The transaction that must be verified
        """

        sender_balance = get_balance(transaction.sender)
        if sender_balance >= transaction.amount:
            return True
        return False

    def check_transactions(self, open_transactions, get_balance):
        return all([self.verify_transaction(transaction, get_balance) for transaction in open_transactions])

