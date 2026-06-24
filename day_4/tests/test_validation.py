from rag_workshop.schemas import Citation, RAGAnswer, RetrievedChunk
from rag_workshop.validation import validate_citations


def test_valid_citation() -> None:
    chunks = [
        RetrievedChunk(
            chunk_id="policy:p1:c1",
            source="policy.pdf",
            page=1,
            text="Frontline agents may approve refunds up to £75.",
            distance=0.1,
        )
    ]
    answer = RAGAnswer(
        answer="The limit is £75.",
        answerable=True,
        citations=[
            Citation(
                chunk_id="policy:p1:c1",
                source="policy.pdf",
                page=1,
                quote="Frontline agents may approve refunds up to £75.",
            )
        ],
    )
    check = validate_citations(answer, chunks)
    assert check.valid
    assert check.errors == []


def test_unretrieved_chunk_is_invalid() -> None:
    answer = RAGAnswer(
        answer="The limit is £75.",
        answerable=True,
        citations=[
            Citation(
                chunk_id="missing",
                source="policy.pdf",
                page=1,
                quote="£75",
            )
        ],
    )
    check = validate_citations(answer, [])
    assert not check.valid
