from abc import ABC, abstractmethod
from typing import Any, Callable

from core.user import User


class Contract(ABC):
    @abstractmethod
    def __init__(self):
        self.name = ""
        self.functions: dict[str, Callable] = {}

    def process(self, function: str, sender: User, **kwargs: dict[str, Any]) -> Any:  # type: ignore
        return self.functions[function](sender=sender, **kwargs)
