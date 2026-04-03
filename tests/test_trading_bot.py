"""
Unit tests for the Trading Bot.

Tests validators, order formatting, and client initialization.
Run with: pytest tests/ -v
"""

import pytest

from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_stop_price,
    validate_all,
)
from bot.orders import format_order_summary, format_order_response


# ═══════════════════════════════════════════════════════════════
#  VALIDATOR TESTS
# ═══════════════════════════════════════════════════════════════


class TestValidateSymbol:
    """Tests for symbol validation."""

    def test_valid_symbol(self):
        assert validate_symbol("BTCUSDT") == "BTCUSDT"

    def test_lowercase_normalized(self):
        assert validate_symbol("ethusdt") == "ETHUSDT"

    def test_whitespace_trimmed(self):
        assert validate_symbol("  BTCUSDT  ") == "BTCUSDT"

    def test_empty_symbol_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_symbol("")

    def test_numeric_symbol_raises(self):
        with pytest.raises(ValueError, match="must contain only letters"):
            validate_symbol("BTC123")

    def test_short_symbol_raises(self):
        with pytest.raises(ValueError, match="too short"):
            validate_symbol("B")


class TestValidateSide:
    """Tests for order side validation."""

    def test_buy(self):
        assert validate_side("BUY") == "BUY"

    def test_sell(self):
        assert validate_side("SELL") == "SELL"

    def test_lowercase_buy(self):
        assert validate_side("buy") == "BUY"

    def test_invalid_side_raises(self):
        with pytest.raises(ValueError, match="must be one of"):
            validate_side("HOLD")

    def test_empty_side_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_side("")


class TestValidateOrderType:
    """Tests for order type validation."""

    def test_market(self):
        assert validate_order_type("MARKET") == "MARKET"

    def test_limit(self):
        assert validate_order_type("LIMIT") == "LIMIT"

    def test_stop_limit(self):
        assert validate_order_type("STOP_LIMIT") == "STOP_LIMIT"

    def test_lowercase(self):
        assert validate_order_type("market") == "MARKET"

    def test_invalid_raises(self):
        with pytest.raises(ValueError, match="must be one of"):
            validate_order_type("FOK")


class TestValidateQuantity:
    """Tests for quantity validation."""

    def test_valid_float(self):
        assert validate_quantity("0.01") == 0.01

    def test_valid_integer_string(self):
        assert validate_quantity("5") == 5.0

    def test_zero_raises(self):
        with pytest.raises(ValueError, match="must be positive"):
            validate_quantity("0")

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="must be positive"):
            validate_quantity("-1")

    def test_non_numeric_raises(self):
        with pytest.raises(ValueError, match="must be a number"):
            validate_quantity("abc")


class TestValidatePrice:
    """Tests for price validation."""

    def test_market_ignores_price(self):
        assert validate_price("100", "MARKET") is None

    def test_market_none_ok(self):
        assert validate_price(None, "MARKET") is None

    def test_limit_valid_price(self):
        assert validate_price("50000", "LIMIT") == 50000.0

    def test_limit_missing_price_raises(self):
        with pytest.raises(ValueError, match="required for LIMIT"):
            validate_price(None, "LIMIT")

    def test_stop_limit_valid_price(self):
        assert validate_price("80000", "STOP_LIMIT") == 80000.0

    def test_stop_limit_missing_price_raises(self):
        with pytest.raises(ValueError, match="required for STOP_LIMIT"):
            validate_price(None, "STOP_LIMIT")

    def test_negative_price_raises(self):
        with pytest.raises(ValueError, match="must be positive"):
            validate_price("-100", "LIMIT")


class TestValidateStopPrice:
    """Tests for stop price validation."""

    def test_non_stop_returns_none(self):
        assert validate_stop_price("100", "MARKET") is None
        assert validate_stop_price("100", "LIMIT") is None

    def test_stop_limit_valid(self):
        assert validate_stop_price("82000", "STOP_LIMIT") == 82000.0

    def test_stop_limit_missing_raises(self):
        with pytest.raises(ValueError, match="required for STOP_LIMIT"):
            validate_stop_price(None, "STOP_LIMIT")

    def test_stop_limit_negative_raises(self):
        with pytest.raises(ValueError, match="must be positive"):
            validate_stop_price("-1", "STOP_LIMIT")


class TestValidateAll:
    """Tests for the combined validation function."""

    def test_market_order(self):
        result = validate_all("BTCUSDT", "BUY", "MARKET", "0.01")
        assert result == ("BTCUSDT", "BUY", "MARKET", 0.01, None, None)

    def test_limit_order(self):
        result = validate_all("ETHUSDT", "SELL", "LIMIT", "0.5", price="2000")
        assert result == ("ETHUSDT", "SELL", "LIMIT", 0.5, 2000.0, None)

    def test_stop_limit_order(self):
        result = validate_all("BTCUSDT", "SELL", "STOP_LIMIT", "0.01", price="80000", stop_price="82000")
        assert result == ("BTCUSDT", "SELL", "STOP_LIMIT", 0.01, 80000.0, 82000.0)

    def test_limit_missing_price_raises(self):
        with pytest.raises(ValueError):
            validate_all("BTCUSDT", "BUY", "LIMIT", "0.01")

    def test_stop_limit_missing_stop_raises(self):
        with pytest.raises(ValueError):
            validate_all("BTCUSDT", "SELL", "STOP_LIMIT", "0.01", price="80000")


# ═══════════════════════════════════════════════════════════════
#  ORDER FORMATTING TESTS
# ═══════════════════════════════════════════════════════════════


class TestFormatOrderSummary:
    """Tests for order request summary formatting."""

    def test_market_summary_contains_fields(self):
        result = format_order_summary("BTCUSDT", "BUY", "MARKET", 0.01, None)
        assert "BTCUSDT" in result
        assert "BUY" in result
        assert "MARKET" in result
        assert "0.01" in result
        assert "Price" not in result  # MARKET has no price line

    def test_limit_summary_contains_price(self):
        result = format_order_summary("ETHUSDT", "SELL", "LIMIT", 0.5, 2000.0)
        assert "Price" in result
        assert "2000.0" in result

    def test_stop_limit_summary_contains_stop_price(self):
        result = format_order_summary("BTCUSDT", "SELL", "STOP_LIMIT", 0.01, 80000.0, 82000.0)
        assert "Stop Price" in result
        assert "82000.0" in result


class TestFormatOrderResponse:
    """Tests for order response formatting."""

    def test_response_contains_all_fields(self):
        response = {
            "orderId": 123456,
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "MARKET",
            "status": "FILLED",
            "executedQty": "0.01",
            "avgPrice": "67000.5",
        }
        result = format_order_response(response)
        assert "123456" in result
        assert "BTCUSDT" in result
        assert "FILLED" in result
        assert "0.01" in result
        assert "67000.5" in result

    def test_response_handles_missing_fields(self):
        response = {}
        result = format_order_response(response)
        assert "N/A" in result  # Missing fields default to N/A
