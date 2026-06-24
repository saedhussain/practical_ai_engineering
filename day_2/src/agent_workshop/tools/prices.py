"""Commodity prices — currently gold via Frankfurter's free FX API.

Frankfurter provides FX rates with XAU (gold) as a valid base.
No API key required.
"""

import httpx
from agents import function_tool

from agent_workshop.config import settings


FRANKFURTER_LATEST_URL = "https://api.frankfurter.dev/v1/latest"


def _get_gold_price(currency: str = "USD") -> str:
    """Get the current gold price per ounce in the given currency.

    Args:
        currency: ISO 4217 currency code (e.g. 'USD', 'GBP', 'EUR').

    Returns:
        A natural-language price summary, or a clear error message.
    """
    if not currency or not currency.strip():
        return "Error: currency code cannot be empty (e.g. 'USD', 'GBP')."

    currency_code = currency.strip().upper()

    try:
        response = httpx.get(
            FRANKFURTER_LATEST_URL,
            params={"base": "XAU", "symbols": currency_code},
            timeout=settings.default_http_timeout,
        )
        response.raise_for_status()
    except httpx.TimeoutException:
        return "Error: Frankfurter request timed out. Try again in a few seconds."
    except httpx.HTTPError as exc:
        return f"Error: gold price fetch failed. Reason: {exc}"

    data = response.json()
    rate = data.get("rates", {}).get(currency_code)
    if rate is None:
        return (
            f"Error: no rate available for {currency_code}. "
            f"Try 'USD', 'EUR', or 'GBP'."
        )

    return f"One ounce of gold is currently {rate:.2f} {currency_code}."


# Agent-facing wrapper.
get_gold_price = function_tool(_get_gold_price)
