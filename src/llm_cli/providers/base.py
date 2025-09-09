from __future__ import annotations
from abc import ABC, abstractmethod


class ProviderError(Exception):
    """Erros relacionados aos provedores de LLM."""


class LLMClient(ABC):
    """Contrato mínimo para qualquer LLM do projeto."""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Gera uma resposta textual para o prompt."""
        raise NotImplementedError
