import chromadb
from chunking.models import Chunk


class ChromaStore:
    def __init__(self, path: str = "./chroma", collection_name: str="vec"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
              configuration={
                "hnsw": {
                    "space": "cosine"
                }
              }
            )

    def upsert(self, embedded_chunks: list[tuple[Chunk, list[float]]]):
        self.collection.upsert(
                ids = [x[0].id for x in embedded_chunks],
                documents = [x[0].content for x in embedded_chunks],
                metadatas = [x[0].metadata.model_dump(mode="json") for x in embedded_chunks],  #mode json for date object
                embeddings = [x[1] for x in embedded_chunks],
        )

    def search( self, query_vector: list[float], n_results: int = 5, where: dict | None = None):
        return self.collection.query(
                    query_embeddings=[query_vector],
                    n_results=n_results,
                    where=where
                )

    def delete_document(self, document_id: str):
        self.collection.delete(where={"document_id": document_id})

    def count(self)->int:
        return self.collection.count()

    def get_relevant_sections(self, document_ids: list[str], sections: list[str]):
        #build the document condition
        if len(document_ids) == 1:
            document_condition = {"document_id": document_ids[0]}
        else:
            document_condition = {
                "$or": [
                    {"document_id": document_id}
                    for document_id in document_ids
                ]
            }

        #build the section condition
        if len(sections) == 1:
            section_condition = {"section": sections[0]}
        else:
            section_condition = {
                "$or": [
                    {"section": section}
                    for section in sections
                ]
            }

        #build the where condition
        where = {
            "$and": [
                document_condition,
                section_condition
            ]
        }

        return self.collection.get(
            where=where
        )
