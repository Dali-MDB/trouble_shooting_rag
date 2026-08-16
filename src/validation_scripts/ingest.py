from chunking.chunker import Chunker
from ingestion.loader import DocumentLoader
from embedding.embedder import Embedder
from vector_store.chroma_store import ChromaStore


loader = DocumentLoader(path="dataset")
chunker = Chunker(max_tokens=500, overlap_tokens=50)
embedder = Embedder()
chromaStore = ChromaStore(collection_name="my_collection")


documents = loader.load_documents()

print("documents:", len(documents))

for doc in documents:
    print(doc.content)
    chunks = chunker.chunk(doc)

    print(doc.id, "chunks:", len(chunks), "\n"*10)

    embeddings = embedder.embed(chunks)
    print(embeddings[0][1])

    print(doc.id, "embeddings:", len(embeddings), "\n"*10)

    chromaStore.upsert(embeddings)


print(chromaStore.count())


