# Binance Futures Testnet Trading Bot

## What This Is

A Python application that allows users to place Market and Limit orders on the Binance Futures Testnet (USDT-M) via a Command Line Interface (CLI). It provides a clean, reusable structure with built-in logging and error handling.

## Core Value

Reliable and structured execution of Binance Futures trades with clear logging, error handling, and input validation via a CLI.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Connect to Binance Futures Testnet (USDT-M) using its dedicated base URL.
- [ ] Support both BUY and SELL sides.
- [ ] Place Market and Limit orders based on user inputs.
- [ ] Accept and validate user input via CLI (symbol, side, order type, quantity, price).
- [ ] Provide a cleanly separated code structure with distinct client/API and command/CLI layers.
- [ ] Implement robust exception handling for invalid input, API errors, and network failures.
- [ ] Log API requests, responses, and errors effectively to a file.
- [ ] Print clear CLI output including order request summary, execution details (orderId, status, executedQty, avgPrice), and success/failure messages.
- [ ] Output necessary log files from at least one MARKET order and one LIMIT order.
- [ ] Create a clear README.md with setup instructions, runnable examples, and assumptions.

### Out of Scope

- Mainnet execution — Application is explicitly restricted to testnet only.
- Automated trading logic — The bot executes specific user-requested orders rather than tracking signals or running algorithms autonomously.

## Context

- **Environment:** Python 3.x.
- **Ecosystem:** Binance Futures Testnet API (`https://testnet.binancefuture.com`).
- **Allowed Libraries:** `python-binance` OR direct REST calls via `requests`/`httpx`. CLI handling via `argparse`, `Typer`, or `Click`.
- **Purpose:** Skill validation for a Python Developer Internship application at Primetrade.ai.

## Constraints

- **Tech Stack:** Must use Python 3.x.
- **Safety:** Must strictly use the Binance Futures Testnet to ensure no real funds are risked.
- **Code Quality:** Expected to deliver clean, reusable, and structured code as per industry standards.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use `click` or `argparse` for CLI | Required by PRD and simplifies CLI parsing and validation. | — Pending |
| Segregated application architecture | Maintain clear boundaries between API client wrapper and order execution logic. | — Pending |

---
*Last updated: 2026-04-03 after project initialization*

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state
