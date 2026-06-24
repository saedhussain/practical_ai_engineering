"""Configuration loaded from the project's .env file.

All environment-dependent values live here, in one Pydantic Settings class.
Tools and scripts import `settings`, never read env vars directly.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# Repo root is two levels above this file: src/agent_workshop/config.py → repo/
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Centralised configuration for the agent workshop.

    Values come from the project's `.env` file. Add new keys here when a new
    tool or agent needs a configurable value — don't read os.environ directly
    from tool code.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API keys
    openai_api_key: str = ""
    tavily_api_key: str = ""

    # Model selection
    openai_model: str = "gpt-4o-mini"

    # Paths
    outputs_dir: Path = PROJECT_ROOT / "outputs"
    sessions_db: Path = PROJECT_ROOT / "chat_history.db"

    # Defaults for tools
    default_search_results: int = 3
    default_http_timeout: float = 10.0


settings = Settings()


# Make the API keys available to libraries that read environ directly
# (the OpenAI Agents SDK does this).
if settings.openai_api_key:
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key
if settings.tavily_api_key:
    os.environ["TAVILY_API_KEY"] = settings.tavily_api_key