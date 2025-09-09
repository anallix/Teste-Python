from __future__ import annotations
from typing import Dict, Tuple
from .base import Strategy

class ShortestWins(Strategy):
    """Escolhe a resposta mais curta. Ignora respostas iniciadas com [ERRO]."""

    def score(self, provider_to_text: Dict[str, str]) -> Tuple[str, str]:
        candidates = {k: v for k, v in provider_to_text.items() if not v.strip().startswith("[ERRO")}
        if not candidates:
        
            k = next(iter(provider_to_text))
            return k, "Todas as respostas falharam; selecionado o primeiro provider disponível."
        best = min(candidates.items(), key=lambda kv: len(kv[1].strip()))
        provider, text = best
        return provider, f"Escolhida a mais curta ({len(text.strip())} caracteres)."
