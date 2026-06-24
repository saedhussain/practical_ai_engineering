from rag_workshop.evaluation import first_relevant_rank, hit_at_k, reciprocal_rank
from rag_workshop.schemas import RetrievedChunk


def make_chunk(source: str) -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=f"{source}:1",
        source=source,
        page=1,
        text="Example",
        distance=0.1,
    )


def test_retrieval_metrics() -> None:
    retrieved = [make_chunk("a.pdf"), make_chunk("b.pdf"), make_chunk("c.pdf")]
    assert hit_at_k(retrieved, ["b.pdf"], k=1) == 0
    assert hit_at_k(retrieved, ["b.pdf"], k=2) == 1
    assert first_relevant_rank(retrieved, ["b.pdf"]) == 2
    assert reciprocal_rank(retrieved, ["b.pdf"]) == 0.5
