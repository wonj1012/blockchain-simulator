from contracts import Contract
from market.actors.user import User
from market.token import Token


class LiquidityPool:
    """
    Represents the a liquidity pool.

    Attributes:
        token_1 (Token): The first token in the liquidity pool.
        token_2 (Token): The second token in the liquidity pool.
        reserve_1 (float): The reserve of the first token in the liquidity pool.
        reserve_2 (float): The reserve of the second token in the liquidity pool.
        fee (float): The fee of the liquidity pool.
    """

    def __init__(
        self,
        token_1: Token,
        token_2: Token,
        fee: float,
        reserve_1: float = 0.0,
        reserve_2: float = 0.0,
    ):
        """
        Initializes a liquidity pool.

        Args:
            token_1 (Token): The first token in the liquidity pool.
            token_2 (Token): The second token in the liquidity pool.
            fee (float): The fee of the liquidity pool.
        """
        self.token_reserve: dict[Token, float] = {}
        self.token_reserve[token_1] = reserve_1
        self.token_reserve[token_2] = reserve_2
        self.fee = fee

    def add_liquidity(self, token: Token, amount: float) -> None:
        """
        Adds liquidity to the liquidity pool.

        Args:
            amount_1 (float): The amount of the first token to add.
            amount_2 (float): The amount of the second token to add.
        """
        self.token_reserve[token] += amount

    def remove_liquidity(self, token: Token, amount: float) -> None:
        """
        Removes liquidity from the liquidity pool.

        Args:
            amount_1 (float): The amount of the first token to remove.
            amount_2 (float): The amount of the second token to remove.
        """
        if self.token_reserve[token] < amount:
            raise ValueError("Insufficient funds")

        self.token_reserve[token] -= amount


class AmmProtocol(Contract):
    """
    Represents a AMM DEX protocol.

    Attributes:
        name (str): The name of the liquidity pool.
        token_1 (Token): The first token in the liquidity pool.
        token_2 (Token): The second token in the liquidity pool.
        reserve_1 (float): The reserve of the first token in the liquidity pool.
        reserve_2 (float): The reserve of the second token in the liquidity pool.
        fee (float): The fee of the liquidity pool.
    """

    def __init__(self, name: str):
        self.name = name
        self.pools: dict[tuple[Token, Token], LiquidityPool] = {}

        self.functions = {
            "swap": self.swap,
            "add_liquidity": self.add_liquidity,
            "remove_liquidity": self.remove_liquidity,
        }

    def create_pool(
        self,
        token_1: Token,
        token_2: Token,
        fee: float,
        reserve_1: float = 0.0,
        reserve_2: float = 0.0,
    ) -> LiquidityPool:
        """
        Creates a liquidity pool.

        Args:
            token_1 (Token): The first token in the liquidity pool.
            token_2 (Token): The second token in the liquidity pool.
            fee (float): The fee of the liquidity pool.
        """
        if token_1 == token_2:
            raise ValueError("Tokens must be different")

        if (token_1, token_2) in self.pools or (token_2, token_1) in self.pools:
            raise ValueError("Liquidity pool already exists")

        new_pool = LiquidityPool(token_1, token_2, fee, reserve_1, reserve_2)

        self.pools[(token_1, token_2)] = new_pool

        return new_pool

    def swap(
        self, sender: User, token_in: Token, token_out: Token, amount_in: float
    ) -> float:
        pool = self._get_pool(token_in, token_out)

        amount_out = self._get_amount_out(pool, token_in, token_out, amount_in)

        sender.remove_from_wallet(token_in, amount_in)
        pool.add_liquidity(token_in, amount_in)

        pool.remove_liquidity(token_out, amount_out)
        sender.add_to_wallet(token_out, amount_out)

        return amount_out

    def add_liquidity(
        self,
        sender: User,
        token_1: Token,
        token_2: Token,
        amount_1: float,
        amount_2: float,
    ):
        pool = self._get_pool(token_1, token_2)

        sender.remove_from_wallet(token_1, amount_1)
        sender.remove_from_wallet(token_2, amount_2)

        pool.add_liquidity(token_1, amount_1)
        pool.add_liquidity(token_2, amount_2)

    def remove_liquidity(
        self,
        sender: User,
        token_1: Token,
        token_2: Token,
        amount_1: float,
        amount_2: float,
    ):
        pool = self._get_pool(token_1, token_2)

        pool.remove_liquidity(token_1, amount_1)
        pool.remove_liquidity(token_2, amount_2)

        sender.add_to_wallet(token_1, amount_1)
        sender.add_to_wallet(token_2, amount_2)

    def _get_pool(self, token_1: Token, token_2: Token) -> LiquidityPool:
        if (token_1, token_2) in self.pools:
            pool = self.pools[(token_1, token_2)]
        elif (token_2, token_1) in self.pools:
            pool = self.pools[(token_2, token_1)]
        else:
            raise ValueError("Liquidity pool does not exist")

        return pool

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
