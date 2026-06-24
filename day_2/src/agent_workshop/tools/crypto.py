"""Crypto price tool — calls the CoinGecko public API.

No API key needed for the simple /price endpoint we use here.
Rate-limited to roughly 30 requests/minute on the free tier.
"""

import httpx
from agents import function_tool

from agent_workshop.config import settings


COINGECKO_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price"


def _get_crypto_price(symbol: str, currency: str = "usd") -> str:
    """Get the current price of a cryptocurrency from CoinGecko.

    Args:
        symbol: the CoinGecko coin id (e.g. 'bitcoin', 'ethereum', 'solana').
        currency: target currency code (default 'usd').

    Returns:
        A natural-language price summary, or a clear error message if the
        call failed. Errors are returned as strings (not raised) so the
        calling agent can react sensibly.
    """
    if not symbol or not symbol.strip():
        return "Error: symbol cannot be empty. Try 'bitcoin' or 'ethereum'."

    params = {"ids": symbol.lower(), "vs_currencies": currency.lower()}

    try:
        response = httpx.get(
            COINGECKO_PRICE_URL,
            params=params,
            timeout=settings.default_http_timeout,
        )
        response.raise_for_status()
    except httpx.TimeoutException:
        return "Error: CoinGecko request timed out. Try again in a few seconds."
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 429:
            return "Error: CoinGecko rate limit hit. Wait 30 seconds before retrying."
        return f"Error: CoinGecko returned HTTP {exc.response.status_code}."
    except httpx.HTTPError as exc:
        return f"Error: could not reach CoinGecko. Reason: {exc}"

    data = response.json()
    if symbol.lower() not in data:
        return (
            f"Error: '{symbol}' is not a recognised CoinGecko id. "
            f"Try 'bitcoin', 'ethereum', or 'solana'."
        )

    price = data[symbol.lower()].get(currency.lower())
    if price is None:
        return f"Error: no {currency.upper()} price available for {symbol}."

    return f"{symbol.capitalize()} is currently {price} {currency.upper()}."


# Agent-facing wrapper.
get_crypto_price = function_tool(_get_crypto_price)
