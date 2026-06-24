"""Weather tool — a stub for demonstration.

In production this would call a real weather API (e.g. OpenWeather, Open-Meteo).
For the workshop we keep it stubbed so students focus on the tool pattern,
not on managing weather-API credentials.
"""

from agents import function_tool


# A small in-memory dataset for a handful of cities.
# Add your own city here if you want to demo a tool extension.
_FAKE_WEATHER = {
    "almaty": "Cold and clear, -3°C",
    "astana": "Heavy snow, -12°C",
    "london": "Overcast with light rain, 8°C",
    "tashkent": "Sunny and mild, 14°C",
    "bishkek": "Partly cloudy, 2°C",
}


def _get_weather(city: str) -> str:
    """Return a stubbed weather summary for a city.

    Args:
        city: city name (case-insensitive).

    Returns:
        A short natural-language weather summary, or a helpful error message
        listing the cities we do have.
    """
    if not city or not city.strip():
        return "Error: city cannot be empty."

    summary = _FAKE_WEATHER.get(city.strip().lower())
    if summary is None:
        available = ", ".join(sorted(_FAKE_WEATHER.keys()))
        return (
            f"Error: no weather data for {city!r}. "
            f"Available cities: {available}."
        )

    return f"Weather in {city.title()}: {summary}"


# Agent-facing wrapper.
get_weather = function_tool(_get_weather)
