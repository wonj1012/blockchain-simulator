from dataclasses import dataclass
from typing import Any, Optional

from contracts.contract import Contract
from market.actors.user import User


@dataclass
class Transaction:
    """
    Represents a transaction within the Diamond Protocol.

    Attributes:
        sender (User): The sender of the transaction.
        contract (Contract): The contract the transaction is sent to.
        function (str): The function of the contract to call.
        args (dict[str, Any]): The arguments to pass to the function.
        gas_fee (Optional[float]): The gas fee of the transaction.
    """

    sender: User
    contract: Contract
    function: str
    args: dict[str, Any]
    gas_fee: Optional[float] = None

    def process(self) -> Any:
        """
        Processes the transaction.
        """
        return self.contract.process(
            function=self.function, sender=self.sender, **self.args
        )
