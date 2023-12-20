from dataclasses import dataclass, field

from contracts.contract import Contract
from core.transaction import Transaction
from market.actors.user import BlockProducer, User
from market.token import Token


@dataclass
class Block:
    block_number: int = 0
    transactions: list[Transaction] = field(default_factory=list)


@dataclass
class Blockchain:
    name: str = "Blockchain"
    blocks: list[Block] = field(default_factory=list)
    mempool: list[Transaction] = field(default_factory=list)
    users: dict[str, User] = field(default_factory=dict)
    tokens: dict[str, Token] = field(default_factory=dict)
    contracts: dict[str, Contract] = field(default_factory=dict)

    @property
    def block_number(self):
        return len(self.blocks)

    def add_transaction(self, transaction: Transaction):
        self.mempool.append(transaction)

    def create_block(self):
        transactions = self.mempool

        for transaction in transactions:
            transaction.process()

        self.mempool = []

        self.blocks.append(Block(self.block_number, transactions))

    def create_user(self, name: str = "") -> User:
        user = User(name)
        self.users[user.address] = user

        return user

    def create_block_producer(self, name: str = "") -> BlockProducer:
        block_producer = BlockProducer(name)
        self.users[block_producer.address] = block_producer

        return block_producer

    def create_token(self, name: str, value: float) -> Token:
        token = Token(name, value)
        self.tokens[token.name] = token

        return token

    def create_contract(self, contract: Contract) -> Contract:
        self.contracts[contract.name] = contract
        contract.connect_blockchain(self)

        return contract
