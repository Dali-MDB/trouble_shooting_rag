from generation.llm import LLM
from generation.generator import Generator
from embedding.embedder import Embedder
from vector_store.chroma_store import ChromaStore
from retrieval.retriever import Retriever
from context.context_builder import ContextBuilder
from rag_service import RAGService

embedder = Embedder()

chromaStore = ChromaStore(collection_name="my_collection")

retriever = Retriever(embedder, chromaStore)

context_builder = ContextBuilder(chromaStore)

generator = Generator()

llm = LLM(model="poolside/laguna-xs-2.1:free")

rag_service = RAGService(
    retriever,
    context_builder,
    generator,
    llm
)


history = []

query = "I am having an issue with an external payment provider becoming slow"

print(rag_service.answer(query, history))


query2 = "What was the root cause?"

print(rag_service.answer(query2, history))