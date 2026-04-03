# Binance Futures Testnet Trading Bot

A Python CLI application for placing **Market**, **Limit**, and **Stop-Limit** orders on the [Binance Futures Testnet (USDT-M)](https://testnet.binancefuture.com). Built with a clean, modular architecture featuring structured logging, comprehensive input validation, and robust error handling.

---

## Features

- **Market, Limit & Stop-Limit Orders** — Place BUY/SELL orders on Binance Futures Testnet
- **Input Validation** — Comprehensive validation of symbol, side, order type, quantity, price, and stop price
- **Structured Logging** — All API requests, responses, and errors logged to `logs/trading_bot.log`
- **Error Handling** — Graceful handling of invalid input, API errors, and network failures
- **Clean Architecture** — Separated API client layer and CLI interface layer
- **Unit Tests** — 42 tests covering validators and formatters (`pytest`)
- **`.env` Support** — Secure credential management via `python-dotenv`

---

## Project Structure

```
trading_bot/
  bot/
    __init__.py          # Package initializer
    client.py            # Binance Futures Testnet API client wrapper
    orders.py            # Order placement logic & formatting
    validators.py        # Input validation functions
    logging_config.py    # Centralized logging configuration
  tests/
    __init__.py          # Test package
    test_trading_bot.py  # Unit tests (42 tests)
  cli.py                 # CLI entry point (argparse)
  requirements.txt       # Python dependencies
  .env.example           # Template for API credentials
  README.md              # This file
  logs/                  # Auto-created log directory
    trading_bot.log      # Execution logs
```

---

## Setup

### 1. Prerequisites

- Python 3.8 or higher
- A [Binance Futures Testnet](https://testnet.binancefuture.com) account

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/trading-bot.git
cd trading-bot
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Credentials

Generate your API key and secret at [https://testnet.binancefuture.com](https://testnet.binancefuture.com).

**Option 1 — `.env` file (recommended):**
```bash
cp .env.example .env
# Edit .env with your actual keys
```

**Option 2 — Environment variables:**
```bash
export BINANCE_TESTNET_API_KEY='your_api_key_here'
export BINANCE_TESTNET_API_SECRET='your_api_secret_here'
```

> **Note:** This bot uses the **Testnet only** — no real funds are ever at risk.

---

## Usage

### Place a Market Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a Limit Order

```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 2000
```

### Place a Stop-Limit Order (Bonus)

```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_LIMIT --quantity 0.01 --price 80000 --stop-price 82000
```

### CLI Help

```bash
python cli.py --help
```

### Run Tests

```bash
python -m pytest tests/ -v
```

---

## Example Output

### Market Order

```
==================================================
  Binance Futures Testnet Trading Bot
==================================================

🔗 Testing Testnet connectivity...
✅ Connected to Binance Futures Testnet.

┌─────────────────────────────────────────┐
│           ORDER REQUEST SUMMARY          │
├─────────────────────────────────────────┤
│  Symbol     : BTCUSDT                   │
│  Side       : BUY                       │
│  Type       : MARKET                    │
│  Quantity   : 0.01                      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│          ORDER RESPONSE DETAILS          │
├─────────────────────────────────────────┤
│  Order ID   : 13020089643               │
│  Symbol     : BTCUSDT                   │
│  Side       : BUY                       │
│  Type       : MARKET                    │
│  Status     : NEW                       │
│  Exec. Qty  : 0.0000                    │
│  Avg. Price : 0.00                      │
└─────────────────────────────────────────┘

✅ Order placed successfully! (ID: 13020089643, Status: NEW)
```

### Limit Order

```
┌─────────────────────────────────────────┐
│           ORDER REQUEST SUMMARY          │
├─────────────────────────────────────────┤
│  Symbol     : ETHUSDT                   │
│  Side       : SELL                      │
│  Type       : LIMIT                     │
│  Quantity   : 0.5                       │
│  Price      : 2000.0                    │
└─────────────────────────────────────────┘

✅ Order placed successfully! (ID: 8630939835, Status: NEW)
```

---

## Logging

All interactions are logged to `logs/trading_bot.log` with rotating file support (5 MB max, 3 backups). Logs include:

- API request parameters
- Response status codes and data
- Error details with stack traces
- Timestamps and source locations

**Sample log entry:**
```
2026-04-03 15:28:22 │ INFO     │ binance_client │ place_order:211 │ Placing BUY MARKET order: BTCUSDT qty=0.010000
2026-04-03 15:28:22 │ DEBUG    │ binance_client │ _request:101 │ REQUEST  POST /fapi/v1/order | params={...}
2026-04-03 15:28:22 │ INFO     │ binance_client │ place_order:222 │ Order response: orderId=13020089643 status=NEW executedQty=0.0000
```

---

## Testing

The project includes **42 unit tests** covering:

| Test Area | Tests | What's Tested |
|-----------|-------|---------------|
| Symbol Validation | 6 | Valid symbols, normalization, empty/invalid input |
| Side Validation | 5 | BUY/SELL, case normalization, invalid input |
| Order Type Validation | 5 | MARKET/LIMIT/STOP_LIMIT, invalid types |
| Quantity Validation | 5 | Positive floats, zero, negative, non-numeric |
| Price Validation | 7 | MARKET (ignored), LIMIT (required), STOP_LIMIT |
| Stop Price Validation | 4 | STOP_LIMIT required, other types ignored |
| Combined Validation | 5 | Full pipeline for all order types |
| Order Formatting | 5 | Summary and response box formatting |

```bash
$ python -m pytest tests/ -v
========================= 42 passed in 0.12s =========================
```

---

## Assumptions

1. **Testnet Only** — This application exclusively targets the Binance Futures Testnet (`https://testnet.binancefuture.com`). It does not support mainnet trading.
2. **Direct REST API** — Uses the `requests` library for direct REST calls instead of the `python-binance` wrapper for transparency and learning purposes.
3. **USDT-M Futures** — Only USDT-margined futures contracts are supported.
4. **Credential Management** — API credentials loaded from `.env` file (via `python-dotenv`) or environment variables. Never hardcoded.
5. **Time-in-Force** — LIMIT and STOP_LIMIT orders default to GTC (Good Till Cancel).
6. **Stop-Limit Implementation** — Uses Binance Futures `STOP` order type which acts as a stop-limit on the futures testnet.

---

## Error Handling

| Error Type | Behavior |
|------------|----------|
| Missing API keys | Clear error message with `.env` setup instructions |
| Invalid input (symbol, side, type, qty, price) | Validation error with specific guidance |
| Network failure | Logged and reported with connection details |
| API error (e.g., insufficient balance) | HTTP error code and Binance error message displayed |
| Testnet unreachable | Connectivity check fails before order attempt |

---

## License

This project was created as part of a Python Developer Internship application task for Primetrade.ai.
