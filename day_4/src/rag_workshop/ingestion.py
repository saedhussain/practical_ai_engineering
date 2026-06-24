from __future__ import annotations

import shutil
from pathlib import Path

import chromadb
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

from rag_workshop.config import settings


def load_documents(data_dir: Path = settings.data_dir) -> list[Document]:
    """Load all PDFs and normalise page-level metadata."""
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory does not exist: {data_dir}")

    documents = PyPDFDirectoryLoader(str(data_dir)).load()
    if not documents:
        raise ValueError(f"No PDF pages were loaded from {data_dir}")

    cleaned: list[Document] = []
    for document in documents:
        text = document.page_content.strip()
        if not text:
            continue

        source = Path(str(document.metadata.get("source", "unknown"))).name
        page = int(document.metadata.get("page", 0)) + 1
        cleaned.append(
            Document(
                page_content=text,
                metadata={"source": source, "page": page},
            )
        )

    if not cleaned:
        raise ValueError("PDFs were found, but no extractable text was produced.")
    return cleaned


def split_documents(
    documents: list[Document],
    chunk_size: int = settings.chunk_size,
    chunk_overlap: int = settings.chunk_overlap,
) -> list[Document]:
    """Split pages into retrieval-sized chunks and add stable IDs."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        source = str(chunk.metadata["source"])
        page = int(chunk.metadata["page"])
        start = int(chunk.metadata.get("start_index", 0))
        chunk.metadata["chunk_id"] = f"{source}:p{page}:s{start}:c{index}"

    return chunks


def embed_chunks(
    chunks: list[Document],
    model: SentenceTransformer,
) -> list[list[float]]:
    """Create normalised local embeddings for all chunk texts."""
    vectors = model.encode(
        [chunk.page_content for chunk in chunks],
        normalize_embeddings=True,
        show_progress_bar=True,
    )
    return vectors.tolist()


def build_collection(
    chunks: list[Document],
    embeddings: list[list[float]],
    *,
    reset: bool = True,
):
    """Create a persistent Chroma collection from precomputed embeddings."""
    if reset and settings.chroma_dir.exists():
        shutil.rmtree(settings.chroma_dir)

    settings.chroma_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(settings.chroma_dir))
    collection = client.get_or_create_collection(
        name=settings.collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    collection.add(
        ids=[str(chunk.metadata["chunk_id"]) for chunk in chunks],
        documents=[chunk.page_content for chunk in chunks],
        embeddings=embeddings,
        metadatas=[
            {
                "source": str(chunk.metadata["source"]),
                "page": int(chunk.metadata["page"]),
                "start_index": int(chunk.metadata.get("start_index", 0)),
            }
            for chunk in chunks
        ],
    )
    return collection


def run_ingestion(*, reset: bool = True) -> dict[str, int]:
    """Run the complete offline ingestion pipeline."""
    documents = load_documents()
    chunks = split_documents(documents)
    model = SentenceTransformer(settings.embedding_model)
    embeddings = embed_chunks(chunks, model)
    collection = build_collection(chunks, embeddings, reset=reset)

    return {
        "pages": len(documents),
        "chunks": len(chunks),
        "stored_records": collection.count(),
        "embedding_dimensions": len(embeddings[0]),
    }
