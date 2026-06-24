"""Tests for the crypto price tool.

Demonstrates the pytest-mock pattern from Section 3.2 of the notebook —
the external HTTP call is replaced with a fake response, so tests run
offline and deterministically.
"""

import httpx
import pytest
from pytest_mock import MockerFixture

from agent_workshop.tools.crypto import _get_crypto_price


def test_returns_price_on_success(mocker: MockerFixture):
    fake_response = mocker.Mock()
    fake_response.json.return_value = {"bitcoin": {"usd": 50000}}
    fake_response.raise_for_status.return_value = None

    mocker.patch(
        "agent_workshop.tools.crypto.httpx.get",
        return_value=fake_response,
    )

    result = _get_crypto_price("bitcoin", "usd")
    assert "50000" in result
    assert "USD" in result


def test_rejects_empty_symbol():
    result = _get_crypto_price("")
    assert result.startswith("Error:")
    assert "empty" in result.lower()


def test_unknown_symbol_returns_helpful_error(mocker: MockerFixture):
    fake_response = mocker.Mock()
    fake_response.json.return_value = {}   # no matching key
    fake_response.raise_for_status.return_value = None

    mocker.patch(
        "agent_workshop.tools.crypto.httpx.get",
        return_value=fake_response,
    )

    result = _get_crypto_price("doesnotexist", "usd")
    assert result.startswith("Error:")
    assert "bitcoin" in result.lower()   # suggests valid alternatives


def test_rate_limit_returns_actionable_error(mocker: MockerFixture):
    fake_response = mocker.Mock()
    fake_response.status_code = 429
    fake_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Too Many Requests",
        request=mocker.Mock(),
        response=fake_response,
    )

    mocker.patch(
        "agent_workshop.tools.crypto.httpx.get",
        return_value=fake_response,
    )

    result = _get_crypto_price("bitcoin", "usd")
    assert result.startswith("Error:")
    assert "rate limit" in result.lower()


def test_timeout_returns_actionable_error(mocker: MockerFixture):
    mocker.patch(
        "agent_workshop.tools.crypto.httpx.get",
        side_effect=httpx.TimeoutException("timed out"),
    )

    result = _get_crypto_price("bitcoin", "usd")
    assert result.startswith("Error:")
    assert "timed out" in result.lower()
