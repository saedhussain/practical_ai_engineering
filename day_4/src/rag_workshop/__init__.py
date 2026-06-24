"""Practical RAG workshop package."""

from rag_workshop.config import settings
from rag_workshop.ingestion import run_ingestion
from rag_workshop.rag import answer_question

__all__ = ["answer_question", "run_ingestion", "settings"]
