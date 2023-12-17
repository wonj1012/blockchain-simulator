from contracts.liquidity_pool import LiquidityPool
from market.actor import User
from market.token import Token


class UniswapV3Pool(LiquidityPool):
    """
    Represents a Uniswap V3 liquidity pool.
    """

    def __init__(self, token_1: Token, token_2: Token, fee: float):
        """
        Initializes a Uniswap V3 liquidity pool.

        Args:
            token_1 (Token): The first token in the liquidity pool.
            token_2 (Token): The second token in the liquidity pool.
            fee (float): The fee of the liquidity pool.
        """
        super().__init__(token_1, token_2, fee)

    def __str__(self) -> str:
        """
        Returns a string representation of the Uniswap V3 liquidity pool.

        Returns:
            str: The string representation of the Uniswap V3 liquidity pool.
        """
        return (
            f"{self.name}\n"
            f"Token 1: {self.pool.token_1}\n"
            f"Token 2: {self.pool.token_2}\n"
            f"Reserve 1: {self.pool.reserve_1}\n"
            f"Reserve 2: {self.pool.reserve_2}\n"
            f"Fee: {self.pool.fee}\n"
        )

    def add_liquidity(self, sender: User, amount_1: float, amount_2: float) -> None:
        """
        Adds liquidity to the Uniswap V3 liquidity pool.

        Args:
            amount_1 (float): The amount of the first token to add.
            amount_2 (float): The amount of the second token to add.
        """
        super().add_liquidity(sender=sender, amount_1=amount_1, amount_2=amount_2)

    def remove_liquidity(self, sender: User, amount_1: float, amount_2: float) -> None:
        """
        Removes liquidity from the Uniswap V3 liquidity pool.

        Args:
            amount_1 (float): The amount of the first token to remove.
            amount_2 (float): The amount of the second token to remove.
        """
        super().remove_liquidity(sender=sender, amount_1=amount_1, amount_2=amount_2)

    def swap(self, sender: User, token_in: Token, amount_in: float) -> float:
        return super().swap(sender=sender, token_in=token_in, amount_in=amount_in)
