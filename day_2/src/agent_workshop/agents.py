"""Agent factory functions.

These build configured agents on demand. Scripts and tests call these
factories rather than creating agents inline — this means agents can be
re-built fresh each run, and tests can override pieces (instructions, tools,
model) without affecting other callers.
"""

from agents import Agent

from agent_workshop.config import settings
from agent_workshop.prompts import (
    ARCHIVIST_INSTRUCTIONS,
    ASSISTANT_INSTRUCTIONS,
    BRIEFER_INSTRUCTIONS,
    EXPLAINER_INSTRUCTIONS,
    RESEARCHER_INSTRUCTIONS,
)
from agent_workshop.tools import (
    get_crypto_price,
    get_gold_price,
    get_weather,
    search_web,
    write_text_file,
    get_currency_rate,
    get_gold_price_usd_per_troy_ounce,

)


def build_assistant(model: str | None = None) -> Agent:
    """Build a general-purpose assistant with all standard tools.

    Args:
        model: override the configured model. Defaults to settings.openai_model.

    Returns:
        A configured Agent.
    """
    return Agent(
        name="Assistant",
        instructions=ASSISTANT_INSTRUCTIONS,
        tools=[get_crypto_price, get_currency_rate,get_gold_price_usd_per_troy_ounce, get_weather, search_web],
        model=model or settings.openai_model,
    )


def build_briefer(model: str | None = None) -> Agent:
    """Build a daily briefing agent with crypto, gold, weather, and search.

    Args:
        model: override the configured model.

    Returns:
        A configured Agent.
    """
    return Agent(
        name="Briefing Assistant",
        instructions=BRIEFER_INSTRUCTIONS,
        tools=[get_crypto_price, get_currency_rate,get_gold_price_usd_per_troy_ounce, get_weather, search_web],
        model=model or settings.openai_model,
    )


def build_researcher_pipeline(model: str | None = None) -> tuple[Agent, Agent, Agent]:
    """Build the three-agent research → explain → archive pipeline.

    Mirrors the multi-agent demo from Section 2.4 of the notebook.

    Args:
        model: override the configured model.

    Returns:
        A tuple of (researcher, explainer, archivist) agents that share a
        session in the calling code.
    """
    from agents import WebSearchTool

    chosen_model = model or settings.openai_model

    researcher = Agent(
        name="Researcher",
        instructions=RESEARCHER_INSTRUCTIONS,
        tools=[WebSearchTool()],
        model=chosen_model,
    )

    explainer = Agent(
        name="Explainer",
        instructions=EXPLAINER_INSTRUCTIONS,
        model=chosen_model,
    )

    archivist = Agent(
        name="Archivist",
        instructions=ARCHIVIST_INSTRUCTIONS,
        tools=[write_text_file],
        model=chosen_model,
    )

    return researcher, explainer, archivist
