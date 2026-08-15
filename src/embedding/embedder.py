from sentence_transformers import SentenceTransformer
from chunking.models import Chunk

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, chunks: list[Chunk])->list[tuple[Chunk, list[float]]]:
        texts = [c.content for c in chunks]
        vectors = self.model.encode(texts)
        #pair the chunks with their corresponding vectors
        return  [(chunk, vector.tolist()) for chunk, vector in zip(chunks, vectors)]

    def embed_query(self, query: str)->list[float]:
        return self.model.encode(query).tolist()
