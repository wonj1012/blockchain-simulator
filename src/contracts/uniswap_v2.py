from contracts.amm_protocol import AmmProtocol, LiquidityPool
from market.token import Token


class UniswapV2(AmmProtocol):
    """
    Represents a Uniswap V2 liquidity pool.
    """

    def __init__(self, name: str = "UniswapV2"):  # type: ignore
        super().__init__(name)

    def _get_amount_out(
        self, pool: LiquidityPool, token_in: Token, token_out: Token, amount_in: float
    ) -> float:
        reserve_in = pool.token_reserve[token_in]
        reserve_out = pool.token_reserve[token_out]

        amount_in_with_fee = amount_in * (1 - pool.fee)

        amount_out = (
            amount_in_with_fee * reserve_out / (reserve_in + amount_in_with_fee)
        )
        return amount_out
