from __future__ import annotations
from typing import List
from .base import Observer

class BestSelection:
    """Mantém o melhor provider e notifica observers ao mudar."""

    def __init__(self) -> None:
        self._best: str | None = None
        self._reason: str = ""
        self._observers: List[Observer] = []

    def attach(self, obs: Observer) -> None:
        self._observers.append(obs)

    def set_best(self, provider: str, reason: str) -> None:
        if provider != self._best or reason != self._reason:
            self._best = provider
            self._reason = reason
            for o in self._observers:
                o.update(provider, reason)

    @property
    def best(self) -> str | None:
        return self._best

    @property
    def reason(self) -> str:
        return self._reason
