from embedding.embedder import Embedder
from vector_store.chroma_store import ChromaStore
from .models import RetrievedChunk
from chunking.models import ChunkMetadata

class Retriever:
    def __init__(self, embedder: Embedder, vector_store: ChromaStore):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, query: str, n_results: int=5, where : dict|None = None)->list[RetrievedChunk]:
        query_vector = self.embedder.embed_query(query)
        result = self.vector_store.search(query_vector, n_results, where)
        response = []
        for i in range(len(result["ids"])):  #we don't use n_results cuz we might have fewer chunks than the requested number
            response.append(RetrievedChunk(
                content=result["documents"][0][i],
                metadata=ChunkMetadata(**result["metadatas"][0][i]),
                distance=result["distances"][0][i]
            ))
        return response
