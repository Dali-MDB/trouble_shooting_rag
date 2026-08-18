from generation.llm import LLM
from generation.generator import Generator
from retrieval.retriever import Retriever
from context.context_builder import ContextBuilder


class RAGService:
    def __init__(
        self,
        retriever: Retriever,
        context_builder: ContextBuilder,
        generator: Generator,
        llm: LLM
    ):
        self.retriever = retriever
        self.context_builder = context_builder
        self.generator = generator
        self.llm = llm


    def answer(self, query: str, history: list|None=None)->str:
        #rewrite the query using the conversation history
        search_query = self.llm.rewrite_query(query, history or [])

        #retrieve relevant chunks using the rewritten query
        retrieved_chunks = self.retriever.retrieve(search_query)

        #build the context from the retrieved chunks
        context = self.context_builder.build(retrieved_chunks)

        #convert the context into a string for the LLM
        knowledge_base = self.generator.context_to_string(context)

        #generate the answer using the original query and conversation history
        return self.llm.answer(query, knowledge_base, history)