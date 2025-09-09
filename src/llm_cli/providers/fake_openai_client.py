from __future__ import annotations
from .base import LLMClient

class FakeOpenAIClient(LLMClient):
    def __init__(self) -> None:
        self.name = "openai-fake"

    def generate(self, prompt: str, **kwargs) -> str:
        criterion = kwargs.get("criterion", "default")
        return (
            f"[{self.name.upper()}] "
            f"Resposta simulada para: {prompt[:80]}... "
            f"(critério: {criterion})"
        )
