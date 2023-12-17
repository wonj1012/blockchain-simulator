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

    def __hash__(self):
        return hash(self.name)


class TokenContainer:
    """
    Represents a container for tokens.

    Attributes:
        tokens (dict[str, Token]): The tokens in the container.
    """

    def __init__(self):
        self.tokens = {}

    def add_token(self, token: Token) -> Token:
        """
        Adds a token to the container.

        Args:
            token (Token): The token to add.

        Returns:
            Token: The added token.
        """
        self.tokens[token.name] = token

        return token

    def get_token(self, name: str) -> Token:
        """
        Gets a token from the container.

        Args:
            name (str): The name of the token.

        Returns:
            Token: The token.
        """
        return self.tokens[name]

    def get_tokens(self) -> list[Token]:
        """
        Gets all tokens from the container.

        Returns:
            list[Token]: The tokens.
        """
        return list(self.tokens.values())

    def __str__(self):
        return f"TokenContainer: {self.tokens}"
