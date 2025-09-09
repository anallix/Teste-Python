from __future__ import annotations
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self) -> int:
        """Executa o comando. Retorna 0 em sucesso."""
        raise NotImplementedError
