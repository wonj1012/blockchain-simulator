from dataclasses import dataclass

from blockchain import Transaction
from contracts import LiquidityPool
from core.user import BlockProducer


@dataclass
class ArbitrageOpportunity:
    """
    Represents an arbitrage opportunity in the Diamond Protocol.

    Attributes:
        block_number (int): The block number at which the arbitrage opportunity occurred.
        pools (list[LiquidityPool]): The pools involved in the arbitrage opportunity.
        potential_profit (float): The potential profit from the arbitrage opportunity.
        required_transactions (list[Transaction]): The transactions required to realize the arbitrage opportunity.
    """

    block_number: int
    pools: list[LiquidityPool]
    potential_profit: float
    required_transactions: list[Transaction]


@dataclass
class Auction:
    """
    Represents an auction for arbitrage opportunities in the Diamond Protocol.

    Attributes:
        auction_id (str): The ID of the auction.
        block_number (int): The block number at which the auction occurred.
        participants (list[BlockProducer]): The block producers participating in the auction.
        bids (dict[BlockProducer, float]): The bids made by the block producers.
        winning_bid (float): The winning bid amount.
    """

    auction_id: str
    block_number: int
    participants: list[BlockProducer]
    bids: dict[BlockProducer, float]
    winning_bid: float
