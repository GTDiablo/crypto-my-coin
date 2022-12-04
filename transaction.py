from dataclasses import dataclass, field
from uuid import uuid4, UUID
import hashlib
import rsa


def pub_key_to_string(pub_key: str) -> bytes:
    return pub_key.save_pkcs1()


ENCYRPT_ALGO = "SHA-1"


@dataclass
class Transaction:
    from_wallet: str
    to_wallet: str
    amount: int
    _id: UUID = field(default_factory=uuid4)
    signature: str = field(default=''.encode('utf-8'))

    def create_signature(self, private_key: str) -> None:
        self.signature = rsa.sign(
            self.hash.encode(), private_key, ENCYRPT_ALGO)

    @property
    def is_valid(self) -> bool:
        valid = False
        try:
            # print('bbbbbbbbbb', self.signature)
            rsa.verify(self.hash, self.signature, self.from_wallet)
            valid = True
        except Exception as error:
            # print('AAAA', error)
            pass
        return valid

    @ property
    def hash(self) -> str:
        m = hashlib.sha256()
        m.update(pub_key_to_string(self.from_wallet))
        m.update(pub_key_to_string(self.to_wallet))
        m.update(self._id.hex.encode('utf-8'))
        m.update(self.amount.to_bytes(2, 'little'))
        return m.hexdigest()


def create_transaction(from_wallet: str, to_wallet: str, amount: int) -> Transaction:
    return Transaction(from_wallet, to_wallet, amount)
