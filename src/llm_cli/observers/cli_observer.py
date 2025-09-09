from __future__ import annotations
from .base import Observer

class CLINotifier(Observer):
    def update(self, best_provider: str, reason: str) -> None:
        print(f"\n[OBSERVADOR] Nova melhor resposta: {best_provider.upper()} — {reason}\n")
