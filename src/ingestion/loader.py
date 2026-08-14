from ingestion.models import Document, DocumentType, MetaData
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def load_documents(path: str)->list[Document]:
    full_path = os.path.join(BASE_DIR , path)
    dirs = os.listdir(full_path)
    result = []
    for item in dirs:
        pth =  os.path.join(full_path, item)
        if os.path.isdir(pth):   #recursive call inside the directory
            result.extend(load_documents(pth))
        else:   #file
            #check the format
            if not item.endswith(".md"):
                continue #ignore

            #treat the file
            with open(pth, 'r') as f:               
                content= f.read()
                #determin type
                file_type = None
                service = None
                severity = None
                environment = None
                date = None
                id = None
                if "dataset/incident" in pth:
                    file_type = DocumentType.INCIDENT
                elif "dataset/architecture" in pth:
                    file_type = DocumentType.ARCHITECTURE
                elif "dataset/runbooks" in pth:
                    file_type = DocumentType.RUNBOOK

                chunks = content.split("\n")
                N = len(chunks)
                #extract id
                for chunk in chunks:
                    chunk = chunk.strip()
                    if chunk:  #not empty
                        id = chunk.removeprefix("# ").strip()
                        break
                if not id:   #invalid document format
                    continue
                #extract meta data
                
                i = 0
                while i < N:
                    chunk = chunks[i].strip()
                    if chunk == "## Service":
                        j = i+1
                        while chunks[j].strip() == "": #empty line
                            j+=1
                        service = chunks[j].strip()
                        i = j+1
                    if chunk == "## Severity":
                        j = i+1
                        while chunks[j].strip() == "": #empty line
                            j+=1
                        severity = chunks[j].strip()
                        i = j+1
                    if chunk == "## Environment":
                        j = i+1
                        while chunks[j].strip() == "": #empty line
                            j+=1
                        environment = chunks[j].strip()
                        i = j+1
                    if chunk == "## Date":
                        j = i+1
                        while chunks[j].strip() == "": #empty line
                            j+=1
                        date = chunks[j].strip()
                        i = j+1
                    i+=1
                metadata = MetaData(service=service, severity=severity, environment=environment, date=date)
                document = Document(id=id, document_type=file_type, content=content, metadata=metadata)
                result.append(document)
    return result
                    



                
                
                