from __future__ import annotations
import os
from typing import Optional, Any
from dotenv import load_dotenv
import requests

from .base import LLMClient, ProviderError

load_dotenv()

class HFTextGenClient(LLMClient):
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "google/flan-t5-base",
        temperature: float = 0.3,
        max_new_tokens: int = 256,
        timeout: int = 60,
    ) -> None:
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise ProviderError("HUGGINGFACE_API_KEY não encontrado (.env).")

        self.model = model
        self.temperature = temperature
        self.max_new_tokens = max_new_tokens
        self.timeout = timeout
        self._endpoint = f"https://api-inference.huggingface.co/models/{self.model}"
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _post(self, payload: dict) -> Any:
        try:
            r = requests.post(self._endpoint, headers=self._headers, json=payload, timeout=self.timeout)
            if r.status_code == 503:
                raise ProviderError(f"Modelo {self.model} está carregando (503). Tente novamente em alguns segundos.")
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise ProviderError(f"HuggingFace erro de rede: {e}") from e

    def generate(self, prompt: str, **kwargs) -> str:
        params = {
            "max_new_tokens": int(kwargs.get("max_new_tokens", self.max_new_tokens)),
            "temperature": float(kwargs.get("temperature", self.temperature)),
        }
        data = self._post({"inputs": prompt, "parameters": params})
        
        if isinstance(data, list) and data:
            item = data[0]
            if isinstance(item, dict) and "generated_text" in item:
                return (item["generated_text"] or "").strip()
        if isinstance(data, dict) and "generated_text" in data:
            return (data["generated_text"] or "").strip()

        raise ProviderError(f"Resposta inesperada da HuggingFace: {data!r}")
