from dataclasses import dataclass, field
from typing import Any, Optional

from contracts import Contract
from market.actors.user import User
from market.token import Token


@dataclass
class Transaction:
    """
    Represents a transaction within the Diamond Protocol.

    Attributes:
        sender (User): The sender of the transaction.
        contract (Contract): The contract the transaction is sent to.
        function (str): The function of the contract to call.
        args (dict[str, Any]): The arguments to pass to the function.
        gas_fee (Optional[float]): The gas fee of the transaction.
    """

    sender: User
    contract: Contract
    function: str
    args: dict[str, Any]
    gas_fee: Optional[float] = None

    def process(self) -> Any:
        """
        Processes the transaction.
        """
        return self.contract.process(
            function=self.function, sender=self.sender, **self.args
        )


@dataclass
class Block:
    block_number: int = 0
    transactions: list[Transaction] = field(default_factory=list)


@dataclass
class Blockchain:
    blocks: list[Block] = field(default_factory=list)
    users: dict[str, User] = field(default_factory=dict)
    tokens: dict[str, Token] = field(default_factory=dict)
    contracts: dict[str, Contract] = field(default_factory=dict)

    @property
    def block_number(self):
        return len(self.blocks)

    def __str__(self):
        return f"Blockchain: {self.blocks}"

    def process_transaction(self, transaction: Transaction):
        transaction.process()

    def create_block(self, transactions: list[Transaction]):
        for transaction in transactions:
            self.process_transaction(transaction)
        block = Block(self.block_number, transactions)
        self.blocks.append(block)

    def create_user(self) -> User:
        user = User()
        self.users[user.address] = user

        return user

    def create_token(self, token: Token) -> Token:
        self.tokens[token.name] = token

        return token

    def create_contract(self, contract: Contract) -> Contract:
        self.contracts[contract.name] = contract

        return contract

    def save_to_file(self, filename: str):
        return None

    @staticmethod
    def load_from_file(filename: str) -> "Blockchain":
        return Blockchain()
