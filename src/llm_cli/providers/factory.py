from __future__ import annotations
from .base import LLMClient, ProviderError


def create_client(kind: str, **kwargs) -> LLMClient:

    if not kind:
        raise ProviderError("Informe o tipo de provider (ex.: 'openai' ou 'hf').")

    k = kind.strip().lower()

    if k in ("openai", "chatgpt", "gpt"):
        from .openai_client import OpenAIChatClient
        return OpenAIChatClient(**kwargs)

    if k in ("openai-fake", "fake", "dummy"):
        from .fake_openai_client import FakeOpenAIClient
        return FakeOpenAIClient()

    if k in ("hf", "huggingface", "t5", "llama", "roberta", "bert"):
        from .hf_client import HFTextGenClient
        return HFTextGenClient(**kwargs)

    raise ProviderError(f"Provider desconhecido: {kind!r}")
