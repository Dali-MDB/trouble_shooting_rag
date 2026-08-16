queries_list = [
    {
        "query": "Which incident was caused by the API Gateway using port 8000 while the Auth Service was listening on port 8080?",
        "expected": "INC-001",
    },
    {
        "query": "Which incident was caused by a missing DATABASE_URL environment variable?",
        "expected": "INC-002",
    },
    {
        "query": "Which incident was caused by authentication sessions being stored in Redis without a TTL?",
        "expected": "INC-003",
    },
    {
        "query": "Which incident was caused by the PostgreSQL connection pool reaching its maximum capacity?",
        "expected": "INC-004",
    },
    {
        "query": "Which incident was caused by an external payment provider becoming slow?",
        "expected": "INC-005",
    },
]
from embedding.embedder import Embedder
from vector_store.chroma_store import ChromaStore
from retrieval.retriever import Retriever

embedder = Embedder()
chromaStore = ChromaStore(collection_name="my_collection")
retriever = Retriever(embedder, chromaStore)



for i in queries_list:
    q = i["query"]
    e = i["expected"]

    answer = retriever.retrieve(q)

    print("QUERY:", q)
    print("EXPECTED:", e)

    for rank, chunk in enumerate(answer, start=1):
        print(
            rank,
            chunk.metadata.document_id,
            chunk.metadata.section,
            chunk.distance
        )
       

    print("----------------------------")