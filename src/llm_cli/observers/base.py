from __future__ import annotations
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, best_provider: str, reason: str) -> None:
        """Notificado quando a melhor resposta muda."""
        raise NotImplementedError
