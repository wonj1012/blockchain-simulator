from dataclasses import dataclass
from core.liquidity_pool import Token


@dataclass
class Transaction:
    """
    Represents a transaction within the Diamond Protocol.

    Attributes:
        sender (str): The address of the sender.
        recipient (str): The address of the recipient.
        amount (float): The amount of the transaction.
        token (Token): The token involved in the transaction.
        block_number (int): The block number at which the transaction occurred.
    """

    block_number: int
    sender: str
    recipient: str
    amount: float
    token: Token
    gas_fee: float
