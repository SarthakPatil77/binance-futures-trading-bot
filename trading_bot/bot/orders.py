import logging

from .client import BinanceClient, BinanceAPIError, NetworkError

logger = logging.getLogger(__name__)


def _format_order_summary(symbol, side, order_type, quantity, price=None, stop_price=None) -> str:
    lines = [
        "┌─────────────── ORDER REQUEST ───────────────┐",
        f"  Symbol     : {symbol}",
        f"  Side       : {side}",
        f"  Type       : {order_type}",
        f"  Quantity   : {quantity}",
    ]
    if price is not None:
        lines.append(f"  Price      : {price}")
    if stop_price is not None:
        lines.append(f"  Stop Price : {stop_price}")
    lines.append("└─────────────────────────────────────────────┘")
    return "\n".join(lines)


def _format_order_response(response: dict) -> str:
    order_id    = response.get("orderId", "N/A")
    status      = response.get("status", "N/A")
    exec_qty    = response.get("executedQty", "0")
    avg_price   = response.get("avgPrice", "N/A")
    client_oid  = response.get("clientOrderId", "N/A")
    symbol      = response.get("symbol", "N/A")
    side        = response.get("side", "N/A")
    order_type  = response.get("type", "N/A")

    lines = [
        "┌─────────────── ORDER RESPONSE ──────────────┐",
        f"  Order ID       : {order_id}",
        f"  Client OID     : {client_oid}",
        f"  Symbol         : {symbol}",
        f"  Side           : {side}",
        f"  Type           : {order_type}",
        f"  Status         : {status}",
        f"  Executed Qty   : {exec_qty}",
        f"  Avg Price      : {avg_price}",
        "└─────────────────────────────────────────────┘",
    ]
    return "\n".join(lines)


def place_market_order(client: BinanceClient, symbol: str, side: str, quantity: float) -> dict:
    """Place a MARKET order on Binance Futures Testnet."""
    logger.info(f"Placing MARKET order: {side} {quantity} {symbol}")
    print(_format_order_summary(symbol, side, "MARKET", quantity))

    try:
        response = client.place_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )
        print(_format_order_response(response))
        print("✅  MARKET order placed successfully!\n")
        logger.info(f"MARKET order success: orderId={response.get('orderId')}, status={response.get('status')}")
        return response

    except BinanceAPIError as e:
        print(f"❌  API Error ({e.code}): {e.message}\n")
        logger.error(f"MARKET order failed — BinanceAPIError {e.code}: {e.message}")
        raise
    except NetworkError as e:
        print(f"❌  Network Error: {e}\n")
        logger.error(f"MARKET order failed — NetworkError: {e}")
        raise


def place_limit_order(client: BinanceClient, symbol: str, side: str, quantity: float, price: float) -> dict:
    """Place a LIMIT order (GTC) on Binance Futures Testnet."""
    logger.info(f"Placing LIMIT order: {side} {quantity} {symbol} @ {price}")
    print(_format_order_summary(symbol, side, "LIMIT", quantity, price=price))

    try:
        response = client.place_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce="GTC",
        )
        print(_format_order_response(response))
        print("✅  LIMIT order placed successfully!\n")
        logger.info(f"LIMIT order success: orderId={response.get('orderId')}, status={response.get('status')}")
        return response

    except BinanceAPIError as e:
        print(f"❌  API Error ({e.code}): {e.message}\n")
        logger.error(f"LIMIT order failed — BinanceAPIError {e.code}: {e.message}")
        raise
    except NetworkError as e:
        print(f"❌  Network Error: {e}\n")
        logger.error(f"LIMIT order failed — NetworkError: {e}")
        raise


def place_stop_market_order(
    client: BinanceClient, symbol: str, side: str, quantity: float, stop_price: float
) -> dict:
    """
    Bonus: Place a STOP_MARKET order on Binance Futures Testnet.
    This triggers a market order when the stop price is hit.
    """
    logger.info(f"Placing STOP_MARKET order: {side} {quantity} {symbol}, stopPrice={stop_price}")
    print(_format_order_summary(symbol, side, "STOP_MARKET", quantity, stop_price=stop_price))

    try:
        response = client.place_order(
            symbol=symbol,
            side=side,
            type="STOP_MARKET",
            quantity=quantity,
            stopPrice=stop_price,
        )
        print(_format_order_response(response))
        print("✅  STOP_MARKET order placed successfully!\n")
        logger.info(f"STOP_MARKET order success: orderId={response.get('orderId')}, status={response.get('status')}")
        return response

    except BinanceAPIError as e:
        print(f"❌  API Error ({e.code}): {e.message}\n")
        logger.error(f"STOP_MARKET order failed — BinanceAPIError {e.code}: {e.message}")
        raise
    except NetworkError as e:
        print(f"❌  Network Error: {e}\n")
        logger.error(f"STOP_MARKET order failed — NetworkError: {e}")
        raise
