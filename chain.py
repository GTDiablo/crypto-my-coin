from typing import List, Union
from block import Block, create_block
from transaction import Transaction
from wallet import Wallet


class Chain:
    ''' '''
    HARDNESS = 2
    TRANSACTIONS_IN_BLOCK = 3

    def __init__(self):
        self.__blocks: List[Block] = [self.__generate_genesis_block()]
        self.__transactions_queue: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        self.__transactions_queue.append(transaction)

        if len(self.__transactions_queue) >= Chain.TRANSACTIONS_IN_BLOCK:
            self.__mine_blocks()

    def get_transaction_queue(self) -> List[Transaction]:
        return [*self.__transactions_queue]

    def __get_last_block(self) -> Block:
        return self.__blocks[-1]

    def __generate_genesis_block(self) -> Block:
        return create_block([], '')

    def __mine_blocks(self) -> None:
        to_mine = self.__transactions_queue[:Chain.TRANSACTIONS_IN_BLOCK]
        last_block = self.__get_last_block()

        self.__transactions_queue = self.__transactions_queue[Chain.TRANSACTIONS_IN_BLOCK:]
        block = create_block(to_mine, last_block.hash)

        block.mine(Chain.HARDNESS)
        self.__blocks.append(block)

    """
    def get_block_by_id(self, block_id: str) -> Union[Block, None]:
        return ''

    def get_transaction_by_id(self, transaction_id: str) -> Union[Transaction, None]:
        return ''
    """

    def len(self) -> int:
        return len(self.__blocks)

    def is_valid(self) -> bool:
        for i in range(1, len(self.__blocks)):
            block = self.__blocks[i]
            prev_block = self.__blocks[i-1]
            if not block.is_valid(Chain.HARDNESS) or block.previous_hash != prev_block.hash:
                return False
        return True

    def get_transactions_by_wallet(self, wallet: Wallet) -> List[Transaction]:
        transactions: List[Transaction] = []
        for block in self.__blocks:
            for transaction in block.transactions:
                if wallet.public_key in [transaction.from_wallet, transaction.to_wallet]:
                    transactions.append(transaction)

        return transactions

    def get_balance(self, wallet: Wallet) -> int:
        balance: int = 0
        transactions: List[Transaction] = self.get_transactions_by_wallet(
            wallet)

        for transaction in transactions:
            if wallet.public_key == transaction.from_wallet:
                balance -= transaction.amount

            if wallet.public_key == transaction.to_wallet:
                balance += transaction.amount

        return balance
