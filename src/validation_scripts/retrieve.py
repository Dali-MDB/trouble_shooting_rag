from embedding.embedder import Embedder
from vector_store.chroma_store import ChromaStore
from retrieval.retriever import Retriever

embedder = Embedder()
chromaStore = ChromaStore(collection_name="my_collection")
retriever = Retriever(embedder, chromaStore)
query = "began returning HTTP 502 Bad Gateway responses for authenticated endpoints"

print(retriever.retrieve(query))
