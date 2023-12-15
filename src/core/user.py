from dataclasses import dataclass

from liquidity_pool import Token
from transaction import Transaction


@dataclass
class User:
    """
    Represents a user of the Diamond Protocol.

    Attributes:
        id (str): The ID of the user.
        wallet (dict[Token, float]): The wallet of the user, containing different tokens.
        transaction_history (list[Transaction]): The transaction history of the user.
    """

    id: str
    wallet: dict[Token, float]
    transaction_history: list[Transaction]


@dataclass
class BlockProducer(User):
    """
    Represents a block producer in the Diamond Protocol.

    Additional Attributes:
        balance (float): The current balance of the block producer.
    """

    balance: float
