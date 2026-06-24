"""Agent workshop package — production-quality refactor of the Day 2 notebook.

Public API:

    from agent_workshop import build_assistant, build_briefer, settings

Lower-level access (for tests, custom agents):

    from agent_workshop.tools.crypto import _get_crypto_price, get_crypto_price
"""

from agent_workshop.agents import build_assistant, build_briefer, build_researcher_pipeline
from agent_workshop.config import settings

__all__ = [
    "build_assistant",
    "build_briefer",
    "build_researcher_pipeline",
    "settings",
]
