from typing import Any
import httpx

from agents import function_tool
from agent_workshop.config import settings

#@function_tool
def _get_currency_rate(base: str, target: str) -> str:
    """
    Get the latest exchange rate between two fiat currencies.

    Args:
        base: Base currency code, such as "GBP".
        target: Target currency code, such as "USD".

    Returns:
        A human-readable result string.
        Example: "1 GBP = 1.2700 USD"

    Notes: 
        Get's data from frankfurter.dev
    """
    base = base.upper().strip()
    target = target.upper().strip()

    if not base or not target:
        return "Error: base and target currency codes are required."

    try:
        response = httpx.get(
            f"https://api.frankfurter.dev/v2/rate/{base}/{target}",
            timeout=settings.default_http_timeout,
        )
        response.raise_for_status()

        data: dict[str, Any] = response.json()
        rate = float(data["rate"])

        return f"1 {base} = {rate:,.4f} {target}"

    except httpx.HTTPError as exc:
        return (
            f"Error: could not fetch the currency rate for {base} to {target}. "
            f"Reason: {exc}"
        )
    except (KeyError, TypeError, ValueError) as exc:
        return (
            f"Error: currency service returned unexpected data for {base} to {target}. "
            f"Reason: {exc}"
        )


# Wrap it as a tool for the agent.
get_currency_rate = function_tool(_get_currency_rate)
