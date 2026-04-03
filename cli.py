#!/usr/bin/env python3
"""
Trading Bot CLI — Entry Point.

Place Market and Limit orders on Binance Futures Testnet (USDT-M)
via a clean command-line interface.

Usage:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
    python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 2000
"""

import argparse
import os
import sys

from bot.client import BinanceTestnetClient
from bot.logging_config import setup_logger
from bot.orders import place_order

logger = setup_logger("cli")


def get_api_credentials() -> tuple:
    """
    Retrieve API credentials from environment variables.

    Returns:
        Tuple of (api_key, api_secret).

    Raises:
        SystemExit: If environment variables are not set.
    """
    api_key = os.environ.get("BINANCE_TESTNET_API_KEY")
    api_secret = os.environ.get("BINANCE_TESTNET_API_SECRET")

    if not api_key or not api_secret:
        print(
            "\n❌ Error: API credentials not found.\n"
            "\n"
            "Please set the following environment variables:\n"
            "  export BINANCE_TESTNET_API_KEY='your_api_key'\n"
            "  export BINANCE_TESTNET_API_SECRET='your_api_secret'\n"
            "\n"
            "Get your keys at: https://testnet.binancefuture.com\n"
        )
        logger.error("Missing API credentials in environment variables.")
        sys.exit(1)

    return api_key, api_secret


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="trading-bot",
        description="Place orders on Binance Futures Testnet (USDT-M)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01\n"
            "  %(prog)s --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 2000\n"
            "\n"
            "Environment Variables:\n"
            "  BINANCE_TESTNET_API_KEY       Your Binance Futures Testnet API key\n"
            "  BINANCE_TESTNET_API_SECRET    Your Binance Futures Testnet API secret\n"
        ),
    )

    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading pair symbol (e.g., BTCUSDT, ETHUSDT)",
    )
    parser.add_argument(
        "--side",
        required=True,
        choices=["BUY", "SELL", "buy", "sell"],
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--type",
        required=True,
        dest="order_type",
        choices=["MARKET", "LIMIT", "market", "limit"],
        help="Order type: MARKET or LIMIT",
    )
    parser.add_argument(
        "--quantity",
        required=True,
        help="Order quantity (e.g., 0.01)",
    )
    parser.add_argument(
        "--price",
        default=None,
        help="Limit price (required for LIMIT orders)",
    )

    return parser


def main():
    """Main entry point for the Trading Bot CLI."""
    parser = build_parser()
    args = parser.parse_args()

    print("\n" + "=" * 50)
    print("  Binance Futures Testnet Trading Bot")
    print("=" * 50)

    # ── Step 1: Load credentials ─────────────────────────────
    api_key, api_secret = get_api_credentials()
    logger.info("API credentials loaded.")

    # ── Step 2: Initialize client ────────────────────────────
    client = BinanceTestnetClient(api_key=api_key, api_secret=api_secret)

    # ── Step 3: Test connectivity ────────────────────────────
    print("\n🔗 Testing Testnet connectivity...")
    if not client.ping():
        print("❌ Cannot reach Binance Futures Testnet. Check your network.")
        logger.error("Testnet connectivity check failed.")
        sys.exit(1)
    print("✅ Connected to Binance Futures Testnet.\n")

    # ── Step 4: Place the order ──────────────────────────────
    try:
        place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValueError as e:
        print(f"\n❌ Validation Error: {e}")
        logger.error("Validation error: %s", e)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Order Failed: {e}")
        logger.error("Order failed: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
