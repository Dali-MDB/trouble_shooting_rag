from context.models import Context
from retrieval.models import RetrievedChunk


class Generator:
    def __init__(self):
        self.section_separator = "\n\n"

    def context_to_string(self, context: Context)->str:
        #convert all documents into one string
        documents = []

        for document_id, chunks in context.documents.items():
            documents.append(self._document_to_string(document_id, chunks))

        return self.section_separator.join(documents)

   
    def _document_to_string(self, document_id: str, chunks: list[RetrievedChunk])->str:
        #convert one document into a string
        sections = []

        for chunk in chunks:
            sections.append(self._chunk_to_string(chunk))

        return f"DOCUMENT: {document_id}\n" + self.section_separator.join(sections)


    def _chunk_to_string(self, chunk: RetrievedChunk)->str:
        #convert one chunk into a string
        return f"{chunk.metadata.section}:\n{chunk.content}"


