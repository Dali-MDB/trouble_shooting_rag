from generation.llm import LLM
from generation.generator import Generator
from embedding.embedder import Embedder
from vector_store.chroma_store import ChromaStore
from retrieval.retriever import Retriever
from context.context_builder import ContextBuilder


embedder = Embedder()
chromaStore = ChromaStore(collection_name="my_collection")
retriever = Retriever(embedder, chromaStore)
context_builder = ContextBuilder(chromaStore)
generator = Generator()
llm = LLM(model="poolside/laguna-xs-2.1:free")

query = "I am having an issue with an external payment provider becoming slow"


answer = retriever.retrieve(query)

context = context_builder.build(answer)
history = []
knowledge_base = generator.context_to_string(context)
print(llm.answer(query, knowledge_base, history))


#test outside of knowledge
query2 = "who won the world cup 2026"
print("__________________________\n\n\n\n\n\n\n\n\n\n\n\n\n")
print(llm.answer(query2, knowledge_base, history))