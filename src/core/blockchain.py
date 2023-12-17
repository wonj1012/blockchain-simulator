from dataclasses import dataclass, field
from typing import Optional

from contracts.contract import Contract
from core.transaction import Transaction
from market.actors.user import User
from market.token import Token


@dataclass
class Block:
    block_number: int = 0
    transactions: list[Transaction] = field(default_factory=list)


@dataclass
class Blockchain:
    blocks: list[Block] = field(default_factory=list)
    mempool: list[Transaction] = field(default_factory=list)
    users: dict[str, User] = field(default_factory=dict)
    tokens: dict[str, Token] = field(default_factory=dict)
    contracts: dict[str, Contract] = field(default_factory=dict)

    @property
    def block_number(self):
        return len(self.blocks)

    def process_transaction(self, transaction: Transaction):
        transaction.process()

    def add_transaction(self, transaction: Transaction):
        self.mempool.append(transaction)

    def create_block(self, transactions: Optional[list[Transaction]] = None):
        if transactions is None:
            transactions = self.mempool
            self.mempool = []

        for transaction in transactions:
            self.process_transaction(transaction)

        self.blocks.append(Block(self.block_number, transactions))

    def create_user(self, name: str = "") -> User:
        user = User(name)
        self.users[user.address] = user

        return user

    def create_token(self, token: Token) -> Token:
        self.tokens[token.name] = token

        return token

    def create_contract(self, contract: Contract) -> Contract:
        self.contracts[contract.name] = contract

        return contract


if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.create_user()
    print(blockchain.users)
