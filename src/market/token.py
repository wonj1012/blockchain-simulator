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

    def __hash__(self):
        return hash(self.name)
