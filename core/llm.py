from abc import ABC, abstractmethod
import requests
from utils.config import CONFIG
from utils.logger import logger

class LLMInterface(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, context: list = None) -> str:
        pass

class OllamaClient(LLMInterface):
    def __init__(self, endpoint: str, model: str):
        self.endpoint = endpoint
        self.model = model

    def generate_response(self, prompt: str, context: list = None) -> str:
        try:
            payload = {"model": self.model, "prompt": prompt}
            if context:
                payload["prompt"] = "Context: " + "\n".join([c["content"] for c in context]) + "\n\n" + prompt
            response = requests.post(f"{self.endpoint}/api/generate", json=payload)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            logger.error(f"LLM error: {e}")
            return "Sorry, I encountered an error while processing your request."

def get_llm_client() -> LLMInterface:
    if CONFIG["LLM_PROVIDER"] == "ollama":
        return OllamaClient(CONFIG["LLM_LOCAL_ENDPOINT"], CONFIG["LLM_MODEL"])
    raise ValueError(f"Unsupported LLM provider: {CONFIG['LLM_PROVIDER']}")
