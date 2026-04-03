# Binance Futures Testnet Trading Bot

A Python CLI application for placing **Market** and **Limit** orders on the [Binance Futures Testnet (USDT-M)](https://testnet.binancefuture.com). Built with a clean, modular architecture featuring structured logging and robust error handling.

---

## Features

- **Market & Limit Orders** — Place BUY/SELL orders on Binance Futures Testnet
- **Input Validation** — Comprehensive validation of symbol, side, order type, quantity, and price
- **Structured Logging** — All API requests, responses, and errors logged to `logs/trading_bot.log`
- **Error Handling** — Graceful handling of invalid input, API errors, and network failures
- **Clean Architecture** — Separated API client layer and CLI interface layer

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
  cli.py                 # CLI entry point (argparse)
  requirements.txt       # Python dependencies
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

Generate your API key and secret at [https://testnet.binancefuture.com](https://testnet.binancefuture.com), then export them:

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

### CLI Help

```bash
python cli.py --help
```

**Output:**
```
usage: trading-bot [-h] --symbol SYMBOL --side {BUY,SELL,buy,sell}
                   --type {MARKET,LIMIT,market,limit} --quantity QUANTITY
                   [--price PRICE]

Place orders on Binance Futures Testnet (USDT-M)

options:
  -h, --help            show this help message and exit
  --symbol SYMBOL       Trading pair symbol (e.g., BTCUSDT, ETHUSDT)
  --side {BUY,SELL}     Order side: BUY or SELL
  --type {MARKET,LIMIT} Order type: MARKET or LIMIT
  --quantity QUANTITY    Order quantity (e.g., 0.01)
  --price PRICE         Limit price (required for LIMIT orders)

Examples:
  trading-bot --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
  trading-bot --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 2000
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
│  Order ID   : 123456789                 │
│  Symbol     : BTCUSDT                   │
│  Side       : BUY                       │
│  Type       : MARKET                    │
│  Status     : FILLED                    │
│  Exec. Qty  : 0.010                     │
│  Avg. Price : 67523.50                  │
└─────────────────────────────────────────┘

✅ Order placed successfully! (ID: 123456789, Status: FILLED)
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
2026-04-03 12:00:00 │ INFO     │ binance_client │ place_order:178 │ Placing BUY MARKET order: BTCUSDT qty=0.010000
2026-04-03 12:00:01 │ INFO     │ binance_client │ place_order:189 │ Order response: orderId=123456789 status=FILLED executedQty=0.010
```

---

## Assumptions

1. **Testnet Only** — This application exclusively targets the Binance Futures Testnet (`https://testnet.binancefuture.com`). It does not support mainnet trading.
2. **Direct REST API** — Uses the `requests` library for direct REST calls instead of the `python-binance` wrapper for transparency and learning purposes.
3. **USDT-M Futures** — Only USDT-margined futures contracts are supported.
4. **Environment Variables** — API credentials are loaded from environment variables for security (never hardcoded).
5. **Time-in-Force** — LIMIT orders default to GTC (Good Till Cancel).

---

## Error Handling

| Error Type | Behavior |
|------------|----------|
| Missing API keys | Clear error message with setup instructions |
| Invalid input (symbol, side, type, qty, price) | Validation error with specific guidance |
| Network failure | Logged and reported with connection details |
| API error (e.g., insufficient balance) | HTTP error code and Binance error message displayed |
| Testnet unreachable | Connectivity check fails before order attempt |

---

## License

This project was created as part of a Python Developer Internship application task.
