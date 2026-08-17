from vector_store.chroma_store import ChromaStore
from retrieval.models import RetrievedChunk
from chunking.models import ChunkMetadata
from .models import Context


class ContextBuilder:
    def __init__(self, vector_store: ChromaStore):
        self.vector_store = vector_store
        self.relevant_sections = ["Investigation", "Root Cause", "Resolution"]
        self.section_order = [
                    "Title",
                    "Service",
                    "Severity",
                    "Environment",
                    "Date",
                    "Symptoms",
                    "Timeline",
                    "Investigation",
                    "Root Cause",
                    "Resolution",
                    "Lessons Learned"
                ]

        

    def build(self, retrieved_chunks: list[RetrievedChunk])->Context:
        #get the documents_ids
        document_ids = self._get_document_ids(retrieved_chunks)

        #retrieve the important sections
        result = self._retrieve_relevant_sections(document_ids)


        #organize chunks by document_id
        grouped = self._group_chunks(result)

        #add the originally retrieved chunks
        self._add_retrieved_chunks(grouped, retrieved_chunks)

        #organize the sections
        self._sort_chunks(grouped)

        return Context(documents=grouped)


    def _get_document_ids(self, retrieved_chunks: list[RetrievedChunk]):
        return list({
            chunk.metadata.document_id
            for chunk in retrieved_chunks
        })


    def _retrieve_relevant_sections(self, document_ids: list[str]):
        return self.vector_store.get_relevant_sections(
            document_ids,
            self.relevant_sections
        )


    def _group_chunks(self, result):
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

        return grouped


    def _add_retrieved_chunks(self, grouped: dict, retrieved_chunks: list[RetrievedChunk]):
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


    def _sort_chunks(self, grouped: dict):
        for document_id in grouped:
            grouped[document_id].sort(
                key=lambda x: (
                    self.section_order.index(x.metadata.section),
                    x.metadata.chunk_index
                )
            )

