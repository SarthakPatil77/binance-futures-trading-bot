import logging

logger = logging.getLogger(__name__)

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


class ValidationError(ValueError):
    pass


def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not symbol or not symbol.isalnum():
        raise ValidationError(f"Invalid symbol '{symbol}'. Must be alphanumeric (e.g., BTCUSDT).")
    logger.debug(f"Symbol validated: {symbol}")
    return symbol


def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}'. Must be one of: {', '.join(VALID_SIDES)}.")
    logger.debug(f"Side validated: {side}")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(f"Invalid order type '{order_type}'. Must be one of: {', '.join(VALID_ORDER_TYPES)}.")
    logger.debug(f"Order type validated: {order_type}")
    return order_type


def validate_quantity(quantity) -> float:
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValidationError(f"Invalid quantity '{quantity}'. Must be a positive number.")
    if qty <= 0:
        raise ValidationError(f"Quantity must be greater than 0. Got: {qty}")
    logger.debug(f"Quantity validated: {qty}")
    return qty


def validate_price(price) -> float:
    try:
        p = float(price)
    except (TypeError, ValueError):
        raise ValidationError(f"Invalid price '{price}'. Must be a positive number.")
    if p <= 0:
        raise ValidationError(f"Price must be greater than 0. Got: {p}")
    logger.debug(f"Price validated: {p}")
    return p


def validate_order_params(symbol, side, order_type, quantity, price=None, stop_price=None):
    symbol     = validate_symbol(symbol)
    side       = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity   = validate_quantity(quantity)

    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        price = validate_price(price)

    if order_type == "STOP_MARKET":
        if stop_price is None:
            raise ValidationError("Stop price (--stop-price) is required for STOP_MARKET orders.")
        stop_price = validate_price(stop_price)

    logger.debug(f"All params validated: symbol={symbol}, side={side}, type={order_type}, qty={quantity}")
    return symbol, side, order_type, quantity, price, stop_price
