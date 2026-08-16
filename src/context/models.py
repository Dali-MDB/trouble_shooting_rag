from pydantic import BaseModel
from retrieval.models import RetrievedChunk

class Context(BaseModel):
    documents: dict[str, list[RetrievedChunk]]