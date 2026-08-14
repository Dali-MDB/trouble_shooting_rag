from pydantic import BaseModel
from datetime import date as Date
from enum import Enum


class MetaData(BaseModel):
    service: str | None = None
    severity: str | None = None
    environment: str | None = None
    date: Date | None = None

class DocumentType(str, Enum):
    INCIDENT = "incident"
    RUNBOOK = "runbook"
    ARCHITECTURE = "architecture"


class Document(BaseModel):
    id: str
    document_type: DocumentType
    content: str
    metadata: MetaData