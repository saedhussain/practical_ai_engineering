
from typing import Any
import httpx
from agents import function_tool

from agent_workshop.config import settings



#@function_tool
def _get_gold_price_usd_per_troy_ounce() -> str:
    """
    Get the latest gold price in USD per troy ounce.

    Returns:
        A human-readable result string.
        Example: "Gold price: $2,350.25 USD per troy ounce"

    Notes:
        Uses Gold API (gold-api.com).
    """

    try:
        response = httpx.get(
            "https://api.gold-api.com/price/XAU",
            timeout=settings.default_http_timeout,
        )
        response.raise_for_status()

        data: dict[str, Any] = response.json()
        price = data["price"]

        return f"Gold price: ${float(price):,.2f} USD per troy ounce"

    except httpx.HTTPError as exc:
        return f"Error: could not fetch the gold price. Reason: {exc}"
    except (KeyError, TypeError, ValueError) as exc:
        return f"Error: gold price service returned unexpected data. Reason: {exc}"
    

# Agent-facing wrapper.
get_gold_price_usd_per_troy_ounce = function_tool(_get_gold_price_usd_per_troy_ounce)
