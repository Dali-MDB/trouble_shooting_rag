from pydantic import BaseModel
from chunking.models import ChunkMetadata

class RetrievedChunk(BaseModel):
    content: str
    metadata: ChunkMetadata
    distance: float