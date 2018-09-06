import hash_util


class Verification:
    @staticmethod  # since it accesses nothing inside the class
    def valid_proof(transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_util.hash_string_256(guess)
        return guess_hash[
               0:2] == '00'  # If generated hash has two leading 0's, it is valid. The condition can be changed.

    @classmethod  # since it accesses valid proof method
    def verify_chain(cls, blockchain):
        is_valid = True

        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_util.hash_block(blockchain[index - 1]):
                is_valid = False
                break
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                is_valid = False
                break

        return is_valid

    @staticmethod  # Since it only works with inputs and doesn't access anything in the class
    def verify_transaction(transaction, get_balance):
        """ Check whether the sender has enough balance to send the the amount.
        Arguments:
            :transaction: The transaction that must be verified
        """

        sender_balance = get_balance(transaction.sender)
        if sender_balance >= transaction.amount:
            return True
        return False

    @classmethod  # Since it accesses a method of the class
    def check_transactions(cls, open_transactions, get_balance):
        return all([cls.verify_transaction(transaction, get_balance) for transaction in open_transactions])

