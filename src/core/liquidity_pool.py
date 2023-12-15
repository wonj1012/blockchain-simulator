from dataclasses import dataclass


@dataclass
class Token:
    """
    Represents a token in the liquidity pools.

    Attributes:
        name (str): The name of the token.
        value (float): The current value of the token.
        total_supply (float): The total supply of the token.
    """

    name: str
    value: float
    total_supply: float


@dataclass
class LiquidityPool:
    """
    Represents a liquidity pool in the Diamond Protocol.

    Attributes:
        token_a (Token): The first token in the pool.
        token_b (Token): The second token in the pool.
        reserve_a (float): The reserve amount of token_a.
        reserve_b (float): The reserve amount of token_b.
    """

    token_a: Token
    token_b: Token
    reserve_a: float
    reserve_b: float

    def add_liquidity(self, amount_a: float, amount_b: float):
        """
        Adds liquidity to the pool.

        Args:
            amount_a (float): Amount of token_a to add.
            amount_b (float): Amount of token_b to add.

        Raises:
            ValueError: If adding amounts are negative.
        """
        if amount_a < 0 or amount_b < 0:
            raise ValueError("Cannot add negative liquidity")
        self.reserve_a += amount_a
        self.reserve_b += amount_b

    def remove_liquidity(self, amount_a: float, amount_b: float):
        """
        Removes liquidity from the pool.

        Args:
            amount_a (float): Amount of token_a to remove.
            amount_b (float): Amount of token_b to remove.

        Raises:
            ValueError: If requested amounts are greater than available reserves.
        """
        if self.reserve_a >= amount_a and self.reserve_b >= amount_b:
            self.reserve_a -= amount_a
            self.reserve_b -= amount_b
        else:
            raise ValueError("Insufficient liquidity")

    def exchange(self, amount: float, from_token: Token, to_token: Token) -> float:
        """
        Exchanges one token for another within the pool.

        Args:
            amount (float): Amount of `from_token` to exchange.
            from_token (Token): The token to exchange from.
            to_token (Token): The token to exchange to.

        Returns:
            float: The amount of `to_token` received in the exchange.

        Raises:
            ValueError: If insufficient reserve or invalid token exchange.
        """
        if from_token == self.token_a and to_token == self.token_b:
            if self.reserve_a > amount:
                exchange_amount = (amount / self.reserve_a) * self.reserve_b
                self.reserve_a -= amount
                self.reserve_b += exchange_amount
                return exchange_amount

            raise ValueError("Insufficient reserve for exchange")

        if from_token == self.token_b and to_token == self.token_a:
            if self.reserve_b > amount:
                exchange_amount = (amount / self.reserve_b) * self.reserve_a
                self.reserve_b -= amount
                self.reserve_a += exchange_amount
                return exchange_amount

            raise ValueError("Insufficient reserve for exchange")

        raise ValueError("Invalid token exchange")

    def get_price(self, token: Token) -> float:
        """
        Get the price of a token in the pool.

        Args:
            token (Token): The token to get the price of.

        Returns:
            float: The price of the token.
        """

        if token == self.token_a:
            return self.reserve_b / self.reserve_a
        if token == self.token_b:
            return self.reserve_a / self.reserve_b

        raise ValueError("Token not in pool.")
