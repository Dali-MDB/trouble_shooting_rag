from ingestion.models import MetaData
from pydantic import BaseModel


class ChunkMetadata(MetaData): #has the extra attributes from MetaData
    document_id: str
    section: str
    chunk_index: int


class Chunk(BaseModel):
    id: str
    content: str
    metadata: ChunkMetadata

