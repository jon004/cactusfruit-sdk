# cactusfruit/sdk/llmserverclient.py
import requests
import logging
from typing import List, Dict, Any

DEFAULT_LLM_SERVER_URL = "http://localhost:8000"
DEFAULT_EMBEDDER_MODEL_PATH = "models/all-MiniLM-L6-v2"

class LlmServerClient:
    def __init__(self, base_url: str = DEFAULT_LLM_SERVER_URL, embedder_model_path: str = DEFAULT_EMBEDDER_MODEL_PATH, generator_model_path: str = DEFAULT_EMBEDDER_MODEL_PATH):
        self.base_url = base_url
        self.embedder_model_path = embedder_model_path
        self.generator_model_path = generator_model_path
        self.logger = logging.getLogger(__name__)

    def _embedder_request(self, url: str, content: str) -> Dict[str, Any]:
        payload = {
            "model_path": self.embedder_model_path,
            "content": content
        }
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()

    def embed_document(self, content: str) -> List[float]:
        data = self._embedder_request(f"{self.base_url}/m/embed/doc", content)
        return data.get("embedding", [])

    def embed_query(self, content: str) -> List[float]:
        data = self._embedder_request(f"{self.base_url}/m/embed/query", content)
        return data.get("embedding", [])

    def embed_token_count(self, content: str) -> int:
        data = self._embedder_request(f"{self.base_url}/m/embed/token/count", content)
        return data.get("token_count", 0)

    def generate(self, role: str, content: str, params: dict = None) -> str:
        payload = {
            "model_path": self.generator_model_path,
            "role": role,
            "content": content,
            **(params or {})
        }
        response = requests.post(f"{self.base_url}/m/prompt", json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
