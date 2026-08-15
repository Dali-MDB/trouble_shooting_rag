from ingestion.models import Document, DocumentType, MetaData
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class DocumentLoader:
    def __init__(self, path: str):
        self.path = os.path.join(BASE_DIR, path)


    def load_documents(self)->list[Document]:
        return self._load_directory(self.path)


    def _load_directory(self, path: str)->list[Document]:
        dirs = os.listdir(path)
        result = []

        for item in dirs:
            pth = os.path.join(path, item)

            if os.path.isdir(pth):   #recursive call inside the directory
                result.extend(self._load_directory(pth))

            else:   #file
                document = self._load_file(pth, item)

                if document:
                    result.append(document)

        return result


    def _load_file(self, path: str, filename: str)->Document | None:
        #check the format
        if not filename.endswith(".md"):
            return None #ignore

        #treat the file
        with open(path, "r") as f:
            content = f.read()

        #determin type
        file_type = self._determine_type(path)

        #extract id
        id = self._extract_id(content)

        if not id:   #invalid document format
            return None

        #extract meta data
        metadata = self._extract_metadata(content)

        return Document(
            id=id,
            document_type=file_type,
            content=content,
            metadata=metadata
        )


    def _determine_type(self, path: str)->DocumentType | None:
        file_type = None

        if "dataset/incident" in path:
            file_type = DocumentType.INCIDENT
        elif "dataset/architecture" in path:
            file_type = DocumentType.ARCHITECTURE
        elif "dataset/runbooks" in path:
            file_type = DocumentType.RUNBOOK

        return file_type


    def _extract_id(self, content: str)->str | None:
        chunks = content.split("\n")

        #extract id
        for chunk in chunks:
            chunk = chunk.strip()

            if chunk:  #not empty
                return chunk.removeprefix("# ").strip()

        return None


    def _extract_metadata(self, content: str)->MetaData:
        chunks = content.split("\n")
        N = len(chunks)

        service = None
        severity = None
        environment = None
        date = None

        i = 0

        while i < N:
            chunk = chunks[i].strip()

            if chunk == "## Service":
                service = self._extract_value(chunks, i)
            elif chunk == "## Severity":
                severity = self._extract_value(chunks, i)
            elif chunk == "## Environment":
                environment = self._extract_value(chunks, i)
            elif chunk == "## Date":
                date = self._extract_value(chunks, i)

            i += 1

        return MetaData(
            service=service,
            severity=severity,
            environment=environment,
            date=date
        )


    def _extract_value(self, chunks: list[str], i: int)->str | None:
        j = i + 1

        while j < len(chunks) and chunks[j].strip() == "": #empty line
            j += 1

        if j >= len(chunks):   #the file ends with empty lines, should be ignored
            return None

        return chunks[j].strip()