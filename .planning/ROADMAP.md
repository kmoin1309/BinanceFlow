# Project Roadmap

**3 phases** | **11 requirements mapped** | All v1 requirements covered ✓

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | Infrastructure | Set up structure, API client, and logging mechanism | CORE-01, REL-01, REL-02 | 3 |
| 2 | Orders & CLI | Implement order endpoints and CLI integration | CORE-02, CORE-03, CLI-01, CLI-02, CLI-03, CLI-04 | 3 |
| 3 | Finalization | Run examples, generate logs, and add documentation | DOC-01, DOC-02, DOC-03 | 3 |

### Phase Details

**Phase 1: Infrastructure**
Goal: Establish project layout, Binance Testnet client wrapper, and centralized logging config with robust error handling.
Requirements: CORE-01, REL-01, REL-02
Success criteria:
1. `client.py` and `logging_config.py` correctly established.
2. Connection to Binance Futures Testnet succeeds with test credentials.
3. Errors are logged to file instead of only crashing.

**Phase 2: Orders & CLI**
Goal: Implement MARKET and LIMIT orders, and wire them up to a functional CLI (e.g., using `argparse`).
Requirements: CORE-02, CORE-03, CLI-01, CLI-02, CLI-03, CLI-04
Success criteria:
1. CLI accepts all required arguments safely.
2. Bot successfully executes MARKET and LIMIT trades via Testnet CLI commands.
3. Terminal shows well-formatted order summary including execution details.

**Phase 3: Finalization**
Goal: Document the bot, gather required logs, and refine package dependencies.
Requirements: DOC-01, DOC-02, DOC-03
Success criteria:
1. `README.md` and `requirements.txt` correctly populated.
2. Logs demonstrating at least one LIMIT and MARKET order are present.
3. Code layout matches recommendations.
