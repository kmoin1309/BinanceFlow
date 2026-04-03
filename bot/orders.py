"""
Order placement logic for the Trading Bot.

Provides a high-level interface for placing validated orders
via the BinanceTestnetClient, with formatted output and logging.
"""

from typing import Any, Dict, Optional

from bot.client import BinanceTestnetClient
from bot.logging_config import setup_logger
from bot.validators import validate_all

logger = setup_logger("orders")


def format_order_summary(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float]) -> str:
    """
    Format a human-readable order request summary.

    Args:
        symbol: Trading pair.
        side: BUY or SELL.
        order_type: MARKET or LIMIT.
        quantity: Order quantity.
        price: Limit price or None.

    Returns:
        Formatted summary string.
    """
    lines = [
        "",
        "┌─────────────────────────────────────────┐",
        "│           ORDER REQUEST SUMMARY          │",
        "├─────────────────────────────────────────┤",
        f"│  Symbol     : {symbol:<25} │",
        f"│  Side       : {side:<25} │",
        f"│  Type       : {order_type:<25} │",
        f"│  Quantity   : {quantity:<25} │",
    ]
    if price is not None:
        lines.append(f"│  Price      : {price:<25} │")
    lines.append("└─────────────────────────────────────────┘")
    lines.append("")

    return "\n".join(lines)


def format_order_response(response: Dict[str, Any]) -> str:
    """
    Format a human-readable order response.

    Args:
        response: API response dictionary from Binance.

    Returns:
        Formatted response string.
    """
    order_id = response.get("orderId", "N/A")
    status = response.get("status", "N/A")
    executed_qty = response.get("executedQty", "N/A")
    avg_price = response.get("avgPrice", response.get("price", "N/A"))
    order_type = response.get("type", "N/A")
    side = response.get("side", "N/A")
    symbol = response.get("symbol", "N/A")

    lines = [
        "",
        "┌─────────────────────────────────────────┐",
        "│          ORDER RESPONSE DETAILS          │",
        "├─────────────────────────────────────────┤",
        f"│  Order ID   : {str(order_id):<25} │",
        f"│  Symbol     : {str(symbol):<25} │",
        f"│  Side       : {str(side):<25} │",
        f"│  Type       : {str(order_type):<25} │",
        f"│  Status     : {str(status):<25} │",
        f"│  Exec. Qty  : {str(executed_qty):<25} │",
        f"│  Avg. Price : {str(avg_price):<25} │",
        "└─────────────────────────────────────────┘",
        "",
    ]

    return "\n".join(lines)


def place_order(
    client: BinanceTestnetClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Validate inputs, place an order, and print formatted results.

    This is the main entry point for order placement — it orchestrates
    validation, API calls, formatted output, and error handling.

    Args:
        client: Initialized BinanceTestnetClient instance.
        symbol: Trading pair (e.g., 'BTCUSDT').
        side: Order side ('BUY' or 'SELL').
        order_type: Order type ('MARKET' or 'LIMIT').
        quantity: Order quantity as string.
        price: Order price as string (required for LIMIT).

    Returns:
        API response dictionary.

    Raises:
        ValueError: If input validation fails.
        requests.exceptions.RequestException: On API/network errors.
    """
    # ── Step 1: Validate all inputs ──────────────────────────
    v_symbol, v_side, v_type, v_qty, v_price = validate_all(symbol, side, order_type, quantity, price)

    # ── Step 2: Print order summary ──────────────────────────
    summary = format_order_summary(v_symbol, v_side, v_type, v_qty, v_price)
    print(summary)
    logger.info("Order request: %s %s %s qty=%.6f price=%s", v_symbol, v_side, v_type, v_qty, v_price)

    # ── Step 3: Place the order ──────────────────────────────
    response = client.place_order(
        symbol=v_symbol,
        side=v_side,
        order_type=v_type,
        quantity=v_qty,
        price=v_price,
    )

    # ── Step 4: Print response details ───────────────────────
    formatted = format_order_response(response)
    print(formatted)

    # ── Step 5: Print success message ────────────────────────
    status = response.get("status", "UNKNOWN")
    order_id = response.get("orderId", "N/A")

    if status in ("NEW", "FILLED", "PARTIALLY_FILLED"):
        print(f"✅ Order placed successfully! (ID: {order_id}, Status: {status})")
        logger.info("Order SUCCESS: orderId=%s status=%s", order_id, status)
    else:
        print(f"⚠️  Order submitted with status: {status} (ID: {order_id})")
        logger.warning("Order status unexpected: orderId=%s status=%s", order_id, status)

    return response
