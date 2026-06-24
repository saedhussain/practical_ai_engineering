from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2] # ← day_4-local


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Day 4 RAG — defaults are fine, override if you want.
    data_dir: Path = PROJECT_ROOT / "data" / "knowledge_base"
    chroma_dir: Path = PROJECT_ROOT / "chroma_db"
    collection_name: str = "asterlane_policies"

    chunk_size: int = 700
    chunk_overlap: int = 100
    top_k: int = 4


settings = Settings()
