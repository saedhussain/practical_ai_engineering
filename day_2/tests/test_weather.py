"""Tests for the weather stub.

No mocking required — this tool is fully in-memory.
Demonstrates testing the simplest possible tool shape.
"""

from agent_workshop.tools.weather import _get_weather


def test_known_city_returns_summary():
    result = _get_weather("Almaty")
    assert "Almaty" in result
    assert "Cold" in result


def test_city_is_case_insensitive():
    assert "Almaty" in _get_weather("almaty")
    assert "Almaty" in _get_weather("ALMATY")
    assert "Almaty" in _get_weather("Almaty")


def test_unknown_city_returns_helpful_error():
    result = _get_weather("Tokyo")
    assert result.startswith("Error:")
    assert "almaty" in result.lower()   # error lists what IS available


def test_empty_city_rejected():
    result = _get_weather("")
    assert result.startswith("Error:")
    assert "empty" in result.lower()


def test_whitespace_city_rejected():
    result = _get_weather("   ")
    assert result.startswith("Error:")
