from dataclasses import dataclass

from contracts import Contract
from core import Token
from core.user import User


@dataclass
class LiquidityPoolStorage:
    """
    Represents the storage of a liquidity pool.

    Attributes:
        token_1 (Token): The first token in the liquidity pool.
        token_2 (Token): The second token in the liquidity pool.
        reserve_1 (float): The reserve of the first token in the liquidity pool.
        reserve_2 (float): The reserve of the second token in the liquidity pool.
        fee (float): The fee of the liquidity pool.
    """

    token_1: Token
    token_2: Token
    reserve_1: float
    reserve_2: float
    lp_token: Token
    fee: float

    def add_liquidity(self, amount_1: float, amount_2: float) -> None:
        """
        Adds liquidity to the liquidity pool.

        Args:
            amount_1 (float): The amount of the first token to add.
            amount_2 (float): The amount of the second token to add.
        """
        self.reserve_1 += amount_1
        self.reserve_2 += amount_2

    def remove_liquidity(self, amount_1: float, amount_2: float) -> None:
        """
        Removes liquidity from the liquidity pool.

        Args:
            amount_1 (float): The amount of the first token to remove.
            amount_2 (float): The amount of the second token to remove.
        """
        self.reserve_1 -= amount_1
        self.reserve_2 -= amount_2


class LiquidityPool(Contract):
    """
    Represents a liquidity pool for the Diamond Protocol.

    Attributes:
        name (str): The name of the liquidity pool.
        token_1 (Token): The first token in the liquidity pool.
        token_2 (Token): The second token in the liquidity pool.
        reserve_1 (float): The reserve of the first token in the liquidity pool.
        reserve_2 (float): The reserve of the second token in the liquidity pool.
        fee (float): The fee of the liquidity pool.
    """

    def __init__(self, token_1: Token, token_2: Token, fee: float):
        lp_token = Token("UNI", 0, 0)

        self.pool = LiquidityPoolStorage(
            token_1=token_1,
            token_2=token_2,
            reserve_1=0,
            reserve_2=0,
            lp_token=lp_token,
            fee=fee,
        )

        self.functions = {
            "swap": self.swap,
            "add_liquidity": self.add_liquidity,
            "remove_liquidity": self.remove_liquidity,
        }

    @property
    def name(self) -> str:
        return f"{self.pool.token_1.name}-{self.pool.token_2.name} LP"

    def swap(self, sender: User, token_in: Token, amount_in: float):
        """
        Swaps a token for another token in the liquidity pool.

        Args:
            token_in (Token): The token to swap for another token.
            amount_in (float): The amount of the token to swap.

        Returns:
            float: The amount of the other token received.
        """
        amount_out = self._get_amount_out(token_in, amount_in)

        sender.remove_from_wallet(token_in, amount_in)
        sender.add_to_wallet(self._get_another_token(token_in), amount_out)

        if token_in == self.pool.token_1:
            self.pool.reserve_1 += amount_in
            self.pool.reserve_2 -= amount_out
        elif token_in == self.pool.token_2:
            self.pool.reserve_2 += amount_in
            self.pool.reserve_1 -= amount_out
        else:
            raise ValueError("Token not in liquidity pool")

        return amount_out

    def add_liquidity(self, sender: User, amount_1: float, amount_2: float):
        """
        Adds liquidity to the liquidity pool.

        Args:
            amount_1 (float): The amount of the first token to add.
            amount_2 (float): The amount of the second token to add.

        Returns:
            float: The amount of liquidity tokens minted.
        """
        sender.remove_from_wallet(self.pool.token_1, amount_1)
        sender.remove_from_wallet(self.pool.token_2, amount_2)

        self.pool.add_liquidity(amount_1, amount_2)

        sender.add_to_wallet(self.pool.lp_token, amount_1 + amount_2)

    def remove_liquidity(self, sender: User, amount_1: float, amount_2: float):
        """
        Removes liquidity from the liquidity pool.

        Args:
            amount_1 (float): The amount of the first token to remove.
            amount_2 (float): The amount of the second token to remove.

        Returns:
            float: The amount of liquidity tokens burned.
        """
        if self.pool.reserve_1 < amount_1 or self.pool.reserve_2 < amount_2:
            raise ValueError("Insufficient funds")

        sender.add_to_wallet(self.pool.token_1, amount_1)
        sender.add_to_wallet(self.pool.token_2, amount_2)

        self.pool.remove_liquidity(amount_1, amount_2)

        sender.wallet[self.pool.lp_token] -= amount_1 + amount_2

    def _get_another_token(self, token: Token) -> Token:
        """
        Gets the other token in the liquidity pool.

        Args:
            token (Token): The token to get the other token for.

        Returns:
            Token: The other token in the liquidity pool.
        """
        if token == self.pool.token_1:
            return self.pool.token_2

        if token == self.pool.token_2:
            return self.pool.token_1

        raise ValueError("Token not in liquidity pool")

    def _get_amount_out(self, token_in: Token, amount_in: float) -> float:
        """
        Gets the amount of the other token received from a swap.

        Args:
            amount_in (float): The amount of the token to swap.

        Returns:
            float: The amount of the other token received.
        """
        if token_in == self.pool.token_1:
            reserve_in = self.pool.reserve_1
            reserve_out = self.pool.reserve_2
        else:
            reserve_in = self.pool.reserve_2
            reserve_out = self.pool.reserve_1

        amount_in_with_fee = amount_in * (1 - self.pool.fee)
        return (amount_in_with_fee * reserve_out) / (reserve_in + amount_in_with_fee)

    def __str__(self) -> str:
        return f"{self.name}:\n\t{self.pool.token_1.name}: {self.pool.reserve_1}\n\t{self.pool.token_2.name}: {self.pool.reserve_2}\n\tLiquidity Tokens: {self.pool.lp_token.total_supply}"
