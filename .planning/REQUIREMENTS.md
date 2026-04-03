# Requirements

## v1 Requirements

### Core Order Placement
- [ ] **CORE-01**: Connect to Binance Futures Testnet (USDT-M) via code separated API client.
- [ ] **CORE-02**: Place Market orders supporting both BUY and SELL sides.
- [ ] **CORE-03**: Place Limit orders supporting both BUY and SELL sides, taking price as a parameter.

### CLI Interface
- [ ] **CLI-01**: Accept input parameters (symbol, side, order type, quantity, price) via arguments using click or argparse.
- [ ] **CLI-02**: Validate all user inputs comprehensively.
- [ ] **CLI-03**: Print clear execution summary with request info and API response data (orderId, status, executedQty, avgPrice).
- [ ] **CLI-04**: Present clear success and failure messages to the user.

### Reliability
- [ ] **REL-01**: Log API requests, responses, and errors to a dedicated log file.
- [ ] **REL-02**: Handle API errors, network failures, and bad inputs gracefully without crashing unsafely.

### Documentation
- [ ] **DOC-01**: Provide README.md detailing setup, examples, and assumptions.
- [ ] **DOC-02**: Generate requirements.txt or pyproject.toml for easy installation.
- [ ] **DOC-03**: Output log files demonstrating successful MARKET and LIMIT orders.

## v2 Requirements
- Add a third order type (Stop-Limit / OCO / TWAP / Grid) (Bonus 1)
- Enhanced CLI UX with interactive menus/prompts (Bonus 2)
- Lightweight UI dashboard (Bonus 3)

## Out of Scope
- Automated algorithmic trading (This bot simply places specific orders requested via CLI).
- Mainnet integration (Must ensure safety by staying strictly on the Testnet).

## Traceability
*(To be populated by Roadmap)*
