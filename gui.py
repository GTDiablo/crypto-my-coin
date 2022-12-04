from enum import Enum
import cmd
import sys
from user_repo import WalletRepo
from chain import Chain
from transaction import Transaction, create_transaction, pub_key_to_string
from wallet import Wallet
from typing import List
from rich.console import Console
from rich.table import Table
from wallet import Wallet, generate_new_wallet
sys.setrecursionlimit(1500)


class Commands(str, Enum):
    SWITCH_USER = 'SWITCH_USER'
    LIST_WALLETS = 'LIST_WALLETS'
    SEND_MONEY = 'SEND_MONEY'
    BUY_COIN = 'BUY_COIN'


class GUI(cmd.Cmd):
    ''' '''
    intro = 'Simple bitcoin implementation (with Merkle tree) by Boda Zsolt'
    prompt = '>> '
    file = None

    def __init__(self, user_repo: WalletRepo, chain: Chain):
        super().__init__()
        self._user_repo = user_repo
        self._chain = chain
        self.current_user = None
        self.console = Console()

    def do_list_wallets(self, args=[]):
        wallets: List[Wallet] = self._user_repo.get_all_wallets()

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column('Name', style="dim")
        table.add_column('Public Key')
        table.add_column('Balance', justify='right')

        for wallet in wallets:
            balance = self._chain.get_balance(wallet)
            table.add_row(wallet.name, wallet.public_key_string, str(balance))

        self.console.print(table)

    def do_create_wallet(self, name: str = None):
        try:
            if not name:
                self.console.print('Please provide name!', style="bold red")
                return

            wallet: Wallet = generate_new_wallet(name)
            self._user_repo.add_wallet(wallet)
            self.console.print(
                f'Generate wallet with name: {name}', style="bold green")

        except ValueError:
            self.console.print(
                'Wallet already exists with this name', style="bold red")

    def do_switch_wallet(self, name: str = ''):
        wallet: Wallet = self._user_repo.get_wallet_by_name(name)
        self.current_user = wallet
        self.console.print(
            f'Changed current user to {wallet.name if wallet else "None"}', style="bold green")

    def do_send_money(self, information: str = ''):
        if not self.current_user:
            self.console.print('Please switch user!', style="bold red")
            return

        to_wallet_name, amount_string = information.split(' ')

        try:
            to_wallet = self._user_repo.get_wallet_by_name(to_wallet_name)
            transaction: Transaction = create_transaction(
                self.current_user.public_key, to_wallet.public_key, int(amount_string))

            transaction.create_signature(self.current_user.private_key)
            self._chain.add_transaction(transaction)

            # f'Added new transaction and it is: {transaction.is_valid}!', style="bold green")
            self.console.print(
                f'Added new transaction!', style="bold green")

        except ValueError as error:
            self.console.print(str(error), style="red")
            self.console.print(
                'No such to wallet or not enough money.', style="bold red")

    def do_buy_coin(self):
        pass

    def do_list_ledger(self, args=''):
        table = Table()

        table.add_column('From')
        table.add_column('To')
        table.add_column('Amount')

        for transaction in self._chain.get_transaction_queue():
            table.add_row(
                pub_key_to_string(transaction.from_wallet).decode(),
                pub_key_to_string(transaction.to_wallet).decode(),
                str(transaction.amount)
            )

        self.console.print(table)

    def do_chain_len(self, args=''):
        chain_len: int = self._chain.len()
        self.console.print(
            f"Number of blocks in the chain: {chain_len}", style="green")

    def do_is_chain_valid(self, args=''):
        self.console.print(
            f'Is current chain valid?: {self._chain.is_valid()}', style="green")

    def do_list_transactions_by_name(self, name: str = ''):
        wallet: Wallet = self._user_repo.get_wallet_by_name(name)

        if not wallet:
            self.console.print(
                'There is no such wallet with this name!', style="red bold")
            return

        transactions: List[Transaction] = self._chain.get_transactions_by_wallet(
            wallet)

        table = Table()

        table.add_column('From')
        table.add_column('To')
        table.add_column('Amount')

        for transaction in transactions:
            table.add_row(
                pub_key_to_string(transaction.from_wallet).decode(),
                pub_key_to_string(transaction.to_wallet).decode(),
                str(transaction.amount)
            )

        self.console.print(table)
