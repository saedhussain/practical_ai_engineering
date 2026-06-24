"""Web search tool — uses Tavily.

Requires TAVILY_API_KEY in the environment (loaded via config.settings).
"""

import httpx
from agents import function_tool

from agent_workshop.config import settings


TAVILY_SEARCH_URL = "https://api.tavily.com/search"


def _search_web(query: str, max_results: int | None = None) -> str:
    """Search the web with Tavily and return a short summary of results.

    Args:
        query: a clear search query.
        max_results: how many results to return (default from settings).

    Returns:
        A formatted summary of the top results, or a clear error message.
    """
    if not query or not query.strip():
        return "Error: search query cannot be empty."

    if not settings.tavily_api_key:
        return "Error: TAVILY_API_KEY is not set in the environment."

    limit = max_results if max_results is not None else settings.default_search_results
    if limit < 1:
        return "Error: max_results must be at least 1."

    try:
        response = httpx.post(
            TAVILY_SEARCH_URL,
            json={
                "api_key": settings.tavily_api_key,
                "query": query,
                "max_results": limit,
            },
            timeout=settings.default_http_timeout * 1.5,
        )
        response.raise_for_status()
    except httpx.TimeoutException:
        return "Error: search timed out. Try again in a few seconds."
    except httpx.HTTPError as exc:
        return f"Error: search failed. Reason: {exc}"

    data = response.json()
    results = data.get("results", [])
    if not results:
        return f"No results found for: {query}"

    lines = []
    for result in results:
        title = result.get("title", "(no title)")
        url = result.get("url", "(no url)")
        snippet = result.get("content", "")[:200]
        lines.append(f"- {title}\n  {url}\n  {snippet}...")

    return f"Top {len(results)} results for '{query}':\n\n" + "\n\n".join(lines)


# Agent-facing wrapper.
search_web = function_tool(_search_web)
