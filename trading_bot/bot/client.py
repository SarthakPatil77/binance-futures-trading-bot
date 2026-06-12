import hashlib
import hmac
import logging
import time
from urllib.parse import urlencode

import requests

logger = logging.getLogger(__name__)

TESTNET_BASE_URL = "https://testnet.binancefuture.com"


class BinanceClient:
    """
    Low-level Binance Futures Testnet REST client.
    Handles authentication (HMAC-SHA256 signature), request dispatch,
    structured logging of requests/responses, and error propagation.
    """

    def __init__(self, api_key: str, api_secret: str, base_url: str = TESTNET_BASE_URL):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })
        logger.info(f"BinanceClient initialized. Base URL: {self.base_url}")

    def _sign(self, params: dict) -> dict:
        """Add HMAC-SHA256 signature to params."""
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _request(self, method: str, endpoint: str, params: dict = None, signed: bool = True):
        """
        Generic request dispatcher.

        Args:
            method:   HTTP method ('GET', 'POST', 'DELETE')
            endpoint: API path, e.g. '/fapi/v1/order'
            params:   Query/body parameters
            signed:   Whether to add timestamp + signature
        """
        params = params or {}
        if signed:
            params = self._sign(params)

        url = f"{self.base_url}{endpoint}"
        logger.debug(f"→ {method} {url} | params: { {k: v for k, v in params.items() if k != 'signature'} }")

        try:
            if method == "GET":
                response = self.session.get(url, params=params, timeout=10)
            elif method == "POST":
                response = self.session.post(url, data=params, timeout=10)
            elif method == "DELETE":
                response = self.session.delete(url, params=params, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            logger.debug(f"← HTTP {response.status_code} | body: {response.text[:500]}")

            if response.status_code != 200:
                try:
                    err = response.json()
                    msg = err.get("msg", response.text)
                    code = err.get("code", response.status_code)
                except Exception:
                    msg = response.text
                    code = response.status_code
                logger.error(f"API error {code}: {msg}")
                raise BinanceAPIError(code=code, message=msg)

            return response.json()

        except requests.exceptions.ConnectionError as e:
            logger.error(f"Network connection error: {e}")
            raise NetworkError(f"Cannot reach Binance testnet. Check your internet connection.\nDetail: {e}") from e
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timed out: {e}")
            raise NetworkError(f"Request timed out after 10 seconds.") from e
        except requests.exceptions.RequestException as e:
            logger.error(f"Unexpected request error: {e}")
            raise NetworkError(f"Unexpected network error: {e}") from e

    def get_server_time(self):
        return self._request("GET", "/fapi/v1/time", signed=False)

    def get_account_info(self):
        return self._request("GET", "/fapi/v2/account")

    def get_exchange_info(self):
        return self._request("GET", "/fapi/v1/exchangeInfo", signed=False)

    def place_order(self, **kwargs):
        return self._request("POST", "/fapi/v1/order", params=kwargs)

    def cancel_order(self, symbol: str, order_id: int):
        return self._request("DELETE", "/fapi/v1/order", params={"symbol": symbol, "orderId": order_id})

    def get_open_orders(self, symbol: str = None):
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._request("GET", "/fapi/v1/openOrders", params=params)


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------

class BinanceAPIError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"Binance API Error {code}: {message}")


class NetworkError(Exception):
    pass
