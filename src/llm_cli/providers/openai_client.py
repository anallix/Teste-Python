from __future__ import annotations
import os
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

from .base import LLMClient, ProviderError

load_dotenv()

class OpenAIChatClient(LLMClient):
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        temperature: float = 0.3,
        base_url: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ProviderError("OPENAI_API_KEY não encontrado (.env).")

        self.model = model
        self.temperature = temperature
        self._client = OpenAI(api_key=self.api_key, base_url=base_url) if base_url else OpenAI(api_key=self.api_key)

    def generate(self, prompt: str, **kwargs) -> str:
        try:
            temperature = float(kwargs.get("temperature", self.temperature))
            model = kwargs.get("model", self.model)

            resp = self._client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            return (resp.choices[0].message.content or "").strip()
        except Exception as e:
            raise ProviderError(f"OpenAI erro: {e}") from e
