"""
Binance Futures Testnet API Client Wrapper.

Encapsulates all communication with the Binance Futures Testnet,
providing a clean interface for placing orders, checking connectivity,
and handling API/network errors gracefully.
"""

import hashlib
import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from bot.logging_config import setup_logger

# ── Constants ────────────────────────────────────────────────
TESTNET_BASE_URL = "https://testnet.binancefuture.com"


class BinanceTestnetClient:
    """
    Client wrapper for the Binance Futures Testnet (USDT-M).

    Handles authentication (HMAC-SHA256 signing), request logging,
    and structured error handling for all API interactions.
    """

    def __init__(self, api_key: str, api_secret: str, base_url: str = TESTNET_BASE_URL):
        """
        Initialize the Binance Testnet client.

        Args:
            api_key: Binance Futures Testnet API key.
            api_secret: Binance Futures Testnet API secret.
            base_url: API base URL (defaults to Testnet).
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.logger = setup_logger("binance_client")

        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })

        self.logger.info("BinanceTestnetClient initialized → %s", self.base_url)

    # ── Signature ────────────────────────────────────────────

    def _sign(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add timestamp and HMAC-SHA256 signature to request parameters.

        Args:
            params: Query parameters to sign.

        Returns:
            Parameters dict with `timestamp` and `signature` appended.
        """
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    # ── HTTP helpers ─────────────────────────────────────────

    def _request(
        self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, signed: bool = False
    ) -> Dict[str, Any]:
        """
        Execute an HTTP request against the Testnet API.

        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint path (e.g. '/fapi/v1/order').
            params: Query or body parameters.
            signed: Whether the request requires authentication.

        Returns:
            Parsed JSON response as a dictionary.

        Raises:
            requests.exceptions.RequestException: On network or HTTP errors.
        """
        url = f"{self.base_url}{endpoint}"
        params = params or {}

        if signed:
            params = self._sign(params)

        self.logger.debug("REQUEST  %s %s | params=%s", method.upper(), endpoint, params)

        try:
            response = self.session.request(method, url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.logger.debug("RESPONSE %s %s | status=%d", method.upper(), endpoint, response.status_code)
            return data

        except requests.exceptions.HTTPError as e:
            error_body = {}
            try:
                error_body = e.response.json()
            except Exception:
                pass
            self.logger.error(
                "HTTP ERROR %s %s | status=%d | code=%s | msg=%s",
                method.upper(),
                endpoint,
                e.response.status_code,
                error_body.get("code", "N/A"),
                error_body.get("msg", str(e)),
            )
            raise

        except requests.exceptions.ConnectionError as e:
            self.logger.error("CONNECTION ERROR %s %s | %s", method.upper(), endpoint, e)
            raise

        except requests.exceptions.Timeout as e:
            self.logger.error("TIMEOUT %s %s | %s", method.upper(), endpoint, e)
            raise

        except requests.exceptions.RequestException as e:
            self.logger.error("REQUEST ERROR %s %s | %s", method.upper(), endpoint, e)
            raise

    # ── Public API ───────────────────────────────────────────

    def ping(self) -> bool:
        """
        Test connectivity to the Binance Futures Testnet.

        Returns:
            True if the server responds successfully, False otherwise.
        """
        try:
            self._request("GET", "/fapi/v1/ping")
            self.logger.info("Ping successful — Testnet is reachable.")
            return True
        except Exception as e:
            self.logger.warning("Ping failed — Testnet unreachable: %s", e)
            return False

    def get_server_time(self) -> Optional[int]:
        """
        Fetch the current server time from Binance Testnet.

        Returns:
            Server timestamp in milliseconds, or None on failure.
        """
        try:
            data = self._request("GET", "/fapi/v1/time")
            server_time = data.get("serverTime")
            self.logger.info("Server time: %s", server_time)
            return server_time
        except Exception as e:
            self.logger.error("Failed to fetch server time: %s", e)
            return None

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        time_in_force: str = "GTC",
    ) -> Dict[str, Any]:
        """
        Place an order on the Binance Futures Testnet.

        Args:
            symbol: Trading pair (e.g., 'BTCUSDT').
            side: Order side — 'BUY' or 'SELL'.
            order_type: Order type — 'MARKET' or 'LIMIT'.
            quantity: Order quantity.
            price: Limit price (required for LIMIT orders).
            time_in_force: Time-in-force policy (default 'GTC' for LIMIT).

        Returns:
            API response dictionary with order details.

        Raises:
            ValueError: If required parameters are missing for the order type.
            requests.exceptions.RequestException: On API/network errors.
        """
        params: Dict[str, Any] = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
        }

        if order_type.upper() == "LIMIT":
            if price is None:
                raise ValueError("Price is required for LIMIT orders.")
            params["price"] = price
            params["timeInForce"] = time_in_force

        self.logger.info(
            "Placing %s %s order: %s qty=%.6f%s",
            side.upper(),
            order_type.upper(),
            symbol.upper(),
            quantity,
            f" @ {price}" if price else "",
        )

        response = self._request("POST", "/fapi/v1/order", params=params, signed=True)

        self.logger.info(
            "Order response: orderId=%s status=%s executedQty=%s",
            response.get("orderId"),
            response.get("status"),
            response.get("executedQty"),
        )

        return response
