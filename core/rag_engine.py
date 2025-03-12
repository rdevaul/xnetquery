from .llm import LLMInterface
from data.store import DocumentStore
from utils.logger import logger

class RagEngine:
    def __init__(self, llm: LLMInterface, store: DocumentStore):
        self.llm = llm
        self.store = store

    def answer(self, query: str) -> str:
        context = self.store.retrieve(query)
        logger.info(f"Retrieved {len(context)} documents for query: {query}")
        return self.llm.generate_response(f"Answer based on XNET documentation: {query}", context)
