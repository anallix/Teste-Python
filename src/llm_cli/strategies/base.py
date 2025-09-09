from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Tuple

class Strategy(ABC):
    @abstractmethod
    def score(self, provider_to_text: Dict[str, str]) -> Tuple[str, str]:
        """
        Recebe {provider: resposta} e retorna (melhor_provider, explicacao).
        """
        raise NotImplementedError
