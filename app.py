from chain import Chain
from user_repo import WalletRepo
from gui import GUI
import sys
sys.setrecursionlimit(1500)


def main():
    wallet_repo = WalletRepo()
    chain = Chain()

    return GUI(wallet_repo, chain)


if __name__ == '__main__':
    sys.setrecursionlimit(1500)
    main().cmdloop()
