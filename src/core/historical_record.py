from dataclasses import dataclass

from core.arbitrage import ArbitrageOpportunity
from core.liquidity_pool import LiquidityPool
from core.transaction import Transaction
from core.user import BlockProducer


@dataclass
class HistoricalRecord:
    """
    Represents a historical record for the simulation.

    Attributes:
        block_number (int): The block number of this historical record.
        liquidity_pools (List[LiquidityPool]): Snapshot of the liquidity pools at this block.
        transactions (List[Transaction]): List of transactions occurred up to this block.
        arbitrage_opportunities (List[ArbitrageOpportunity]): Detected arbitrage opportunities at this block.
        block_producer_actions (List[BlockProducer]): Actions taken by block producers at this block.

    """

    block_number: int
    liquidity_pools: list[LiquidityPool]
    transactions: list[Transaction]
    arbitrage_opportunities: list[ArbitrageOpportunity]
    block_producer_actions: list[BlockProducer]
