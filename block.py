from dataclasses import dataclass, field
from transaction import Transaction
from typing import List, Union
from uuid import uuid4, UUID
from merkle_tree import MerkleTree
import hashlib


@dataclass
class Block:
    transactions: List[Transaction]
    timestamp: int
    previous_hash: str
    nonce: int = field(default=0)
    _id: UUID = field(default_factory=uuid4)

    def mine(self, hardness: int) -> None:
        while not self.is_valid(hardness):
            self.nonce += 1

    def is_valid(self, hardness: int):
        return '0' * hardness == self.hash[:hardness]

    @property
    def merkle_tree_root(self):
        tree = MerkleTree(self.transactions)
        return tree.root

    @property
    def hash(self) -> str:
        h = hashlib.sha256()
        # TODO: TIMESTAMP
        h.update(self.merkle_tree_root)
        h.update(self.previous_hash.encode('utf-8'))
        h.update(self.nonce.to_bytes(2, 'big'))
        h.update(self._id.hex.encode('utf-8'))
        digest = h.hexdigest()
        print('Block Digest', digest)
        return digest


def create_block(transactions: List[Transaction], previous_hash: str) -> Block:
    timestamp = ''
    return Block(transactions, timestamp, previous_hash)
