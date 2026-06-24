from pydantic import BaseModel, Field


class RetrievedChunk(BaseModel):
    chunk_id: str
    source: str
    page: int
    text: str
    distance: float


class Citation(BaseModel):
    chunk_id: str = Field(description="ID of a retrieved chunk supporting the answer.")
    source: str = Field(description="Source PDF filename.")
    page: int = Field(description="One-based PDF page number.")
    quote: str = Field(description="A short exact quotation from the cited chunk.")


class RAGAnswer(BaseModel):
    answer: str = Field(description="Answer based only on the retrieved context.")
    answerable: bool = Field(
        description="True only when the retrieved context contains enough evidence."
    )
    citations: list[Citation] = Field(
        default_factory=list,
        description="Evidence citations for material claims.",
    )


class CitationCheck(BaseModel):
    valid: bool
    errors: list[str] = Field(default_factory=list)


class RAGResult(BaseModel):
    question: str
    answer: RAGAnswer
    retrieved_chunks: list[RetrievedChunk]
    citation_check: CitationCheck
