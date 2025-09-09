from __future__ import annotations
from typing import Dict, Tuple, Iterable
from .base import Strategy
from .length import ShortestWins

class KeywordsCoverage(Strategy):
    """
    Escolhe quem cobre mais palavras-chave (case-insensitive).
    Empate: desempata pela mais curta.
    """

    def __init__(self, keywords: Iterable[str]) -> None:
        self.keywords = [k.lower() for k in keywords if k.strip()]

    def score(self, provider_to_text: Dict[str, str]) -> Tuple[str, str]:
        if not self.keywords:
            return ShortestWins().score(provider_to_text)

        def coverage(text: str) -> int:
            low = text.lower()
            return sum(1 for k in self.keywords if k in low)

        candidates = {k: v for k, v in provider_to_text.items() if not v.strip().startswith("[ERRO")}
        if not candidates:
            k = next(iter(provider_to_text))
            return k, "Todas as respostas falharam; selecionado o primeiro provider disponível."

        best = sorted(candidates.items(), key=lambda kv: (-coverage(kv[1]), len(kv[1].strip())))
        provider, text = best[0]
        cov = coverage(text)
        return provider, f"Maior cobertura de palavras-chave ({cov}/{len(self.keywords)})."
