from vector_store.chroma_store import ChromaStore
from retrieval.models import RetrievedChunk
from chunking.models import ChunkMetadata
from .models import Context


class ContextBuilder:
    def __init__(self, vector_store: ChromaStore)->Context:
        self.vector_store = vector_store
        self.relevant_sections = ["Investigation", "Root Cause", "Resolution"]
        self.section_order = [
                    "Title",
                    "Symptoms",
                    "Timeline",
                    "Investigation",
                    "Root Cause",
                    "Resolution",
                    "Lessons Learned"
                ]

    def build(self, retrieved_chunks: list[RetrievedChunk]):
        #get the documents_ids
        document_ids = list({
            chunk.metadata.document_id
            for chunk in retrieved_chunks
        })

        #retrieve the important sections
        result = self.vector_store.get_relevant_sections(
            document_ids,
            self.relevant_sections
        )

        #organize chunks by document_id
        grouped = {}

        for i in range(len(result["ids"])):
            chunk = RetrievedChunk(
                content=result["documents"][i],
                metadata=ChunkMetadata(**result["metadatas"][i]),
                distance=0
            )

            document_id = chunk.metadata.document_id

            if document_id in grouped:
                grouped[document_id].append(chunk)
            else:  #first item
                grouped[document_id] = [chunk]

        #add the originally retrieved chunks
        for chunk in retrieved_chunks:
            document_id = chunk.metadata.document_id

            #check if the chunk already exists
            exists = any(
                x.metadata.chunk_index == chunk.metadata.chunk_index
                and x.metadata.section == chunk.metadata.section
                for x in grouped[document_id]
            )

            if not exists:
                grouped[document_id].append(chunk)

        #organize the sections
        for document_id in grouped:
            grouped[document_id].sort(
                key=lambda x: (
                    self.section_order.index(x.metadata.section),
                    x.metadata.chunk_index
                )
            )

        return Context(grouped)