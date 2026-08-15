from transformers import AutoTokenizer
from .models import ChunkMetadata, Chunk
from ingestion.models import Document, MetaData



class Chunker:
    def __init__(self, max_tokens: int, overlap_tokens: int):
        if max_tokens <= 0:
            raise ValueError("max_tokens must be greater than 0")

        if overlap_tokens < 0 or overlap_tokens >= max_tokens:
            raise ValueError("overlap_tokens must be >= 0 and < max_tokens")

        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens

        #tokenizer is used to count and split tokens, NOT to generate embeddings
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

        self.sections = {
                            "## Title",
                            "## Service",
                            "## Severity",
                            "## Environment",
                            "## Date",
                            "## Symptoms",
                            "## Timeline",
                            "## Investigation",
                            "## Root Cause",
                            "## Resolution",
                            "## Lessons Learned"
                        }



    def chunk(self, document: Document)->list[Chunk]:
        sections = self._extract_sections(document.content)

        result = []
        chunk_index = 0

        for section_name, section_content in sections:
            chunks = self._split_section(section_content)

            for chunk in chunks:
                result.append(self._create_chunk(
                    document_id=document.id,
                    section=section_name,
                    chunk_index=chunk_index,
                    meta_data=document.metadata,
                    id=f"{document.id}-{chunk_index}",
                    content=chunk
                ))

                chunk_index += 1

        return result
                


    def _extract_sections(self, text: str)->list[tuple[str, str]]:
        content = text.split("\n")
        sections = []

        current_section = None
        current_content = []

        for c in content:
            c = c.strip()

            if not c:
                continue

            if c in self.sections: #we entered a new section

                #check if not the first section => we need to save the previous section
                if current_section is not None:
                    sections.append(
                        (
                            current_section,
                            "\n".join(current_content)
                        )
                    )

                #start the new section
                current_section = c.removeprefix("## ").strip()
                current_content = []

            else: #useful line
                current_content.append(c)

        #save the last section because the loop has ended
        if current_section is not None:
            sections.append(
                (
                    current_section,
                    "\n".join(current_content)
                )
            )

        return sections
        

    def _split_section(self, section: str)->list[str]:
        tokens = self.tokenizer.encode(
            section,
            add_special_tokens=False
        )

        N = len(tokens)

        if N <= self.max_tokens:
            return [section]

        chunks = []

        i = 0
        step = self.max_tokens - self.overlap_tokens

        while i < N:
            end = i + self.max_tokens

            chunk_tokens = tokens[i:end]

            #convert token IDs back into text
            chunk_text = self.tokenizer.decode(
                chunk_tokens,
                skip_special_tokens=True
            )

            chunks.append(chunk_text)

            i += step

        return chunks



    def _create_chunk(self,document_id: str,section: str,chunk_index: int,meta_data: MetaData,id: str,content: str,)->Chunk:

        chunk_meta_data = ChunkMetadata(
                document_id=document_id,
                section=section,
                chunk_index=chunk_index,
                service=meta_data.service,
                severity=meta_data.severity,
                environment=meta_data.environment,
                date=meta_data.date
                )

        return Chunk(
            id=id,
            content=content,
            metadata=chunk_meta_data
        )