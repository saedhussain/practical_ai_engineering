from rag_workshop.schemas import CitationCheck, RAGAnswer, RetrievedChunk


def validate_citations(
    answer: RAGAnswer,
    retrieved_chunks: list[RetrievedChunk],
) -> CitationCheck:
    """Check that generated citations refer to retrieved evidence."""
    chunk_map = {chunk.chunk_id: chunk for chunk in retrieved_chunks}
    errors: list[str] = []

    if answer.answerable and not answer.citations:
        errors.append("Answer is marked answerable but contains no citations.")

    if not answer.answerable and answer.citations:
        errors.append("Unanswerable response should not contain evidence citations.")

    for citation in answer.citations:
        chunk = chunk_map.get(citation.chunk_id)
        if chunk is None:
            errors.append(f"Chunk was not retrieved: {citation.chunk_id}")
            continue

        if citation.source != chunk.source:
            errors.append(f"Source mismatch for {citation.chunk_id}")

        if citation.page != chunk.page:
            errors.append(f"Page mismatch for {citation.chunk_id}")

        quote = " ".join(citation.quote.split()).casefold()
        chunk_text = " ".join(chunk.text.split()).casefold()
        if quote and quote not in chunk_text:
            errors.append(f"Quote not found in chunk {citation.chunk_id}")

    return CitationCheck(valid=not errors, errors=errors)
