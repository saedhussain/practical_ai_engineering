from __future__ import annotations

import os

import chromadb
from agents import Agent, Runner
from sentence_transformers import SentenceTransformer

from rag_workshop.config import settings
from rag_workshop.schemas import RAGAnswer, RAGResult, RetrievedChunk
from rag_workshop.validation import validate_citations


def load_runtime():
    """Load the embedding model and persistent Chroma collection."""
    if not settings.chroma_dir.exists():
        raise FileNotFoundError(
            "The Chroma database does not exist. Run scripts/ingest.py first."
        )

    model = SentenceTransformer(settings.embedding_model)
    client = chromadb.PersistentClient(path=str(settings.chroma_dir))
    collection = client.get_collection(settings.collection_name)
    return model, collection


def retrieve_context(
    question: str,
    *,
    top_k: int = settings.top_k,
    model: SentenceTransformer | None = None,
    collection=None,
) -> list[RetrievedChunk]:
    """Retrieve the top-k chunks for a question."""
    if model is None or collection is None:
        model, collection = load_runtime()

    query_embedding = model.encode(
        question,
        normalize_embeddings=True,
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    chunks: list[RetrievedChunk] = []
    for chunk_id, text, metadata, distance in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
        strict=True,
    ):
        chunks.append(
            RetrievedChunk(
                chunk_id=chunk_id,
                source=str(metadata["source"]),
                page=int(metadata["page"]),
                text=text,
                distance=float(distance),
            )
        )
    return chunks


def build_context(chunks: list[RetrievedChunk]) -> str:
    """Format retrieved chunks for the generation prompt."""
    sections = []
    for chunk in chunks:
        sections.append(
            f"[chunk_id={chunk.chunk_id} | source={chunk.source} | page={chunk.page}]\n"
            f"{chunk.text}"
        )
    return "\n\n---\n\n".join(sections)


def build_prompt(question: str, chunks: list[RetrievedChunk]) -> str:
    context = build_context(chunks)
    return f"""Use only the retrieved context below.

Rules:
- Do not use outside knowledge.
- If the context is insufficient, set answerable to false and explain briefly.
- If answerable is true, cite the retrieved chunks that support material claims.
- Every quote must be copied exactly from its cited chunk.
- Use the chunk_id, source and page exactly as provided.

RETRIEVED CONTEXT
{context}

USER QUESTION
{question}
"""


def create_answer_agent() -> Agent:
    if not settings.openai_api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add a key."
        )

    os.environ["OPENAI_API_KEY"] = settings.openai_api_key
    return Agent(
        name="AsterLane grounded policy assistant",
        model=settings.openai_model,
        instructions=(
            "You answer questions about AsterLane documents. "
            "Use only the supplied retrieved context. "
            "Return a concise structured answer with verifiable citations."
        ),
        output_type=RAGAnswer,
    )


async def generate_answer(
    question: str,
    chunks: list[RetrievedChunk],
    *,
    agent: Agent | None = None,
) -> RAGAnswer:
    """Generate a structured answer from retrieved evidence."""
    agent = agent or create_answer_agent()
    run = await Runner.run(agent, build_prompt(question, chunks))
    output = run.final_output
    if not isinstance(output, RAGAnswer):
        raise TypeError("Agent did not return the expected RAGAnswer object.")
    return output


async def answer_question(
    question: str,
    *,
    top_k: int = settings.top_k,
) -> RAGResult:
    """Run retrieval, structured generation and citation validation."""
    chunks = retrieve_context(question, top_k=top_k)
    answer = await generate_answer(question, chunks)
    citation_check = validate_citations(answer, chunks)

    return RAGResult(
        question=question,
        answer=answer,
        retrieved_chunks=chunks,
        citation_check=citation_check,
    )
