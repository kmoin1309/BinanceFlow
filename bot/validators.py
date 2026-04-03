"""
Input validators for the Trading Bot CLI.

Provides reusable validation functions for all user-supplied
parameters: symbol, side, order type, quantity, price, and stop price.
"""

from typing import Optional, Tuple

# ── Valid values ─────────────────────────────────────────────
VALID_SIDES = ("BUY", "SELL")
VALID_ORDER_TYPES = ("MARKET", "LIMIT", "STOP_LIMIT")


def validate_symbol(symbol: str) -> str:
    """
    Validate and normalize a trading pair symbol.

    Args:
        symbol: Raw user input for the trading pair.

    Returns:
        Uppercase symbol string.

    Raises:
        ValueError: If symbol is empty or contains invalid characters.
    """
    if not symbol or not symbol.strip():
        raise ValueError("Symbol cannot be empty.")

    cleaned = symbol.strip().upper()

    if not cleaned.isalpha():
        raise ValueError(f"Invalid symbol '{symbol}' — must contain only letters (e.g., BTCUSDT).")

    if len(cleaned) < 2:
        raise ValueError(f"Invalid symbol '{symbol}' — too short.")

    return cleaned


def validate_side(side: str) -> str:
    """
    Validate the order side.

    Args:
        side: Raw user input for order side.

    Returns:
        Uppercase side string ('BUY' or 'SELL').

    Raises:
        ValueError: If side is not BUY or SELL.
    """
    if not side or not side.strip():
        raise ValueError("Side cannot be empty.")

    cleaned = side.strip().upper()

    if cleaned not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}' — must be one of: {', '.join(VALID_SIDES)}.")

    return cleaned


def validate_order_type(order_type: str) -> str:
    """
    Validate the order type.

    Args:
        order_type: Raw user input for order type.

    Returns:
        Uppercase order type string ('MARKET', 'LIMIT', or 'STOP_LIMIT').

    Raises:
        ValueError: If order type is not valid.
    """
    if not order_type or not order_type.strip():
        raise ValueError("Order type cannot be empty.")

    cleaned = order_type.strip().upper()

    if cleaned not in VALID_ORDER_TYPES:
        raise ValueError(f"Invalid order type '{order_type}' — must be one of: {', '.join(VALID_ORDER_TYPES)}.")

    return cleaned


def validate_quantity(quantity: str) -> float:
    """
    Validate and parse the order quantity.

    Args:
        quantity: Raw user input for quantity.

    Returns:
        Positive float value.

    Raises:
        ValueError: If quantity is not a valid positive number.
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid quantity '{quantity}' — must be a number.")

    if qty <= 0:
        raise ValueError(f"Quantity must be positive, got {qty}.")

    return qty


def validate_price(price: Optional[str], order_type: str) -> Optional[float]:
    """
    Validate the price parameter based on order type.

    Args:
        price: Raw user input for price (may be None for MARKET orders).
        order_type: Already-validated order type.

    Returns:
        Positive float for LIMIT/STOP_LIMIT orders, None for MARKET orders.

    Raises:
        ValueError: If price is missing for LIMIT/STOP_LIMIT orders or not a valid positive number.
    """
    if order_type.upper() == "MARKET":
        return None

    # LIMIT and STOP_LIMIT orders require price
    if price is None:
        raise ValueError(f"Price is required for {order_type} orders.")

    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid price '{price}' — must be a number.")

    if p <= 0:
        raise ValueError(f"Price must be positive, got {p}.")

    return p


def validate_stop_price(stop_price: Optional[str], order_type: str) -> Optional[float]:
    """
    Validate the stop/trigger price for STOP_LIMIT orders.

    Args:
        stop_price: Raw user input for stop price.
        order_type: Already-validated order type.

    Returns:
        Positive float for STOP_LIMIT orders, None otherwise.

    Raises:
        ValueError: If stop price is missing for STOP_LIMIT or invalid.
    """
    if order_type.upper() != "STOP_LIMIT":
        return None

    if stop_price is None:
        raise ValueError("Stop price is required for STOP_LIMIT orders.")

    try:
        sp = float(stop_price)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid stop price '{stop_price}' — must be a number.")

    if sp <= 0:
        raise ValueError(f"Stop price must be positive, got {sp}.")

    return sp


def validate_all(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str] = None,
    stop_price: Optional[str] = None,
) -> Tuple[str, str, str, float, Optional[float], Optional[float]]:
    """
    Validate all order parameters at once.

    Args:
        symbol: Trading pair (e.g., 'BTCUSDT').
        side: Order side ('BUY' or 'SELL').
        order_type: Order type ('MARKET', 'LIMIT', or 'STOP_LIMIT').
        quantity: Order quantity as string.
        price: Order price as string (required for LIMIT/STOP_LIMIT).
        stop_price: Stop trigger price (required for STOP_LIMIT).

    Returns:
        Tuple of validated (symbol, side, order_type, quantity, price, stop_price).

    Raises:
        ValueError: If any parameter fails validation.
    """
    v_symbol = validate_symbol(symbol)
    v_side = validate_side(side)
    v_type = validate_order_type(order_type)
    v_qty = validate_quantity(quantity)
    v_price = validate_price(price, v_type)
    v_stop = validate_stop_price(stop_price, v_type)

    return v_symbol, v_side, v_type, v_qty, v_price, v_stop
