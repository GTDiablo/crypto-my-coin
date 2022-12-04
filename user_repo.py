from wallet import Wallet
from typing import List, Union, Dict


class WalletRepo:
    def __init__(self):
        self.__wallets: Dict[str, Wallet] = {}

    def add_wallet(self, wallet: Wallet) -> Wallet:

        wallet_in_repo = self.__wallets.get(wallet.name, None)

        if wallet_in_repo:
            raise ValueError('Wallet name with this name is already exists!')

        self.__wallets[wallet.name] = wallet

        return wallet

    def get_wallet_by_name(self, wallet_name: str) -> Union[Wallet, None]:
        return self.__wallets.get(wallet_name, None)

    def get_all_wallets(self) -> List[Wallet]:
        return self.__wallets.values()
