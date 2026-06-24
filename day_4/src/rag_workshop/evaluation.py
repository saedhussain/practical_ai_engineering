from __future__ import annotations

from collections.abc import Iterable

from rag_workshop.schemas import RetrievedChunk


def hit_at_k(
    retrieved: list[RetrievedChunk],
    expected_sources: Iterable[str],
    *,
    k: int,
) -> int:
    """Return 1 when any expected source appears in the first k results."""
    expected = set(expected_sources)
    return int(any(chunk.source in expected for chunk in retrieved[:k]))


def first_relevant_rank(
    retrieved: list[RetrievedChunk],
    expected_sources: Iterable[str],
) -> int | None:
    """Return the one-based rank of the first expected source."""
    expected = set(expected_sources)
    for rank, chunk in enumerate(retrieved, start=1):
        if chunk.source in expected:
            return rank
    return None


def reciprocal_rank(
    retrieved: list[RetrievedChunk],
    expected_sources: Iterable[str],
) -> float:
    rank = first_relevant_rank(retrieved, expected_sources)
    return 0.0 if rank is None else 1.0 / rank
