import os
import yaml
from sentence_transformers import SentenceTransformer
import faiss
from utils.logger import logger

class DocumentStore:
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(embedding_model)
        self.index = faiss.IndexFlatL2(384)  # MiniLM-L6 dimension
        self.documents = []

    def load_documents(self, folder: str = "data/documents"):
        for file in os.listdir(folder):
            filepath = os.path.join(folder, file)
            if file.endswith(".yaml") or file.endswith(".yml"):
                with open(filepath, "r") as f:
                    data = yaml.safe_load(f)
                    text = yaml.dump(data)
            elif file.endswith(".txt"):
                with open(filepath, "r") as f:
                    text = f.read()
            else:
                continue
            self._add_document(text)

    def _add_document(self, text: str):
        embedding = self.model.encode(text)
        self.index.add(embedding.reshape(1, -1))
        self.documents.append({"content": text})
        logger.info(f"Added document with {len(text)} characters")

    def retrieve(self, query: str, k: int = 3) -> list:
        query_embedding = self.model.encode(query)
        distances, indices = self.index.search(query_embedding.reshape(1, -1), k)
        return [self.documents[i] for i in indices[0]]
