from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

from llm_cli.commands.base import Command
from llm_cli.providers.factory import create_client
from llm_cli.providers.base import ProviderError

from llm_cli.strategies.base import Strategy
from llm_cli.strategies.length import ShortestWins
from llm_cli.strategies.keywords import KeywordsCoverage

from llm_cli.observers.selection import BestSelection
from llm_cli.observers.cli_observer import CLINotifier

@dataclass
class AskCommandPayload:
    prompt: str
    providers: List[str] = field(default_factory=lambda: ["openai", "openai-fake"])
    temperature: float = 0.3
    strategy: str = "keywords"         
    keywords: List[str] = field(default_factory=list)

class AskCommand(Command):
    """Encapsula a ação 'perguntar' (Command)."""

    def __init__(self, payload: AskCommandPayload) -> None:
        self.payload = payload

    def _make_strategy(self) -> Strategy:
        if self.payload.strategy == "shortest":
            return ShortestWins()
        return KeywordsCoverage(self.payload.keywords)

    def execute(self) -> int:
        prompt = self.payload.prompt
        results: Dict[str, str] = {}

        # 1) consulta todos os providers
        for name in self.payload.providers:
            try:
                client = create_client(name, temperature=self.payload.temperature)
                results[name] = client.generate(prompt)
            except ProviderError as e:
                results[name] = f"[ERRO] {e}"

        # 2) mostra respostas brutas
        print(f"\nPergunta: {prompt}\n")
        for name, text in results.items():
            print(f"=== {name.upper()} ===")
            print(text, end="\n\n")

        # 3) aplica Strategy
        strategy = self._make_strategy()
        best_provider, reason = strategy.score(results)

        # 4) Observer: notifica mudança de melhor resposta
        selection = BestSelection()
        selection.attach(CLINotifier())
        selection.set_best(best_provider, reason)

        print(">>> ESCOLHA FINAL")
        print(f"Provider: {best_provider.upper()}")
        print(f"Motivo:   {reason}")

        return 0
