import uuid
from dataclasses import dataclass, field

from market.token import Token


@dataclass
class User:
    """
    Represents a user of the Diamond Protocol.

    Attributes:
        address (str): The address of the user.
        wallet (dict[Token, float]): The wallet of the user, containing different tokens.
        transaction_history (list[Transaction]): The transaction history of the user.
    """

    name: str
    address: str = field(default_factory=lambda: str(uuid.uuid4()))
    wallet: dict[Token, float] = field(default_factory=dict)

    @property
    def total_value(self) -> float:
        """
        Returns the total value of the user's wallet.
        """
        return sum(token.value * amount for token, amount in self.wallet.items())

    def send_transaction(
        self, transaction: "Transaction", blockchain: "Blockchain"  # type: ignore
    ) -> None:
        blockchain.add_transaction(transaction)

    def add_to_wallet(self, token: Token, amount: float) -> None:
        """
        Adds a token to the user's wallet.

        Args:
            token (Token): The token to add.
            amount (float): The amount of the token to add.
        """
        if amount < 0:
            raise ValueError("Amount must be positive")

        if token not in self.wallet:
            self.wallet[token] = 0.0

        self.wallet[token] += amount

    def remove_from_wallet(self, token: Token, amount: float) -> None:
        """
        Removes a token from the user's wallet.

        Args:
            token (Token): The token to remove.
            amount (float): The amount of the token to remove.
        """
        if amount < 0:
            raise ValueError("Amount must be positive")

        if token not in self.wallet:
            raise ValueError("Token not in wallet")

        if self.wallet[token] < amount:
            raise ValueError("Insufficient funds")

        self.wallet[token] -= amount

        if self.wallet[token] == 0:
            del self.wallet[token]


@dataclass
class BlockProducer(User):
    """
    Represents a block producer in the Diamond Protocol.

    Additional Attributes:
        balance (float): The current balance of the block producer.
    """

    balance: float = 0.0
