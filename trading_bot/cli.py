#!/usr/bin/env python3
"""
trading_bot/cli.py
──────────────────
CLI entry point for the Binance Futures Testnet trading bot.

Usage examples:
  python cli.py place --symbol BTCUSDT --side BUY  --type MARKET --quantity 0.001
  python cli.py place --symbol BTCUSDT --side SELL --type LIMIT  --quantity 0.001 --price 50000
  python cli.py place --symbol BTCUSDT --side BUY  --type STOP_MARKET --quantity 0.001 --stop-price 58000
  python cli.py account
  python cli.py open-orders --symbol BTCUSDT
"""

import argparse
import os
import sys

from bot.logging_config import setup_logging
from bot.client import BinanceClient, BinanceAPIError, NetworkError
from bot.orders import place_market_order, place_limit_order, place_stop_market_order
from bot.validators import validate_order_params, ValidationError


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def get_client() -> BinanceClient:
    api_key    = os.environ.get("BINANCE_API_KEY", "").strip()
    api_secret = os.environ.get("BINANCE_API_SECRET", "").strip()

    if not api_key or not api_secret:
        print(
            "❌  Missing credentials.\n"
            "    Set BINANCE_API_KEY and BINANCE_API_SECRET as environment variables.\n"
            "    Example:\n"
            "      export BINANCE_API_KEY=your_key\n"
            "      export BINANCE_API_SECRET=your_secret\n"
        )
        sys.exit(1)

    return BinanceClient(api_key=api_key, api_secret=api_secret)


# ──────────────────────────────────────────────────────────────────────────────
# Sub-command handlers
# ──────────────────────────────────────────────────────────────────────────────

def cmd_place(args):
    import logging
    logger = logging.getLogger(__name__)

    try:
        symbol, side, order_type, quantity, price, stop_price = validate_order_params(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )
    except ValueError as e:
        print(f"❌  Validation Error: {e}\n")
        logger.error(f"Validation failed: {e}")
        sys.exit(1)

    client = get_client()

    try:
        if order_type == "MARKET":
            place_market_order(client, symbol, side, quantity)
        elif order_type == "LIMIT":
            place_limit_order(client, symbol, side, quantity, price)
        elif order_type == "STOP_MARKET":
            place_stop_market_order(client, symbol, side, quantity, stop_price)
    except (BinanceAPIError, NetworkError):
        sys.exit(1)


def cmd_account(args):
    client = get_client()
    try:
        info = client.get_account_info()
        print("\n── Account Info ──────────────────────────────")
        print(f"  Can Trade    : {info.get('canTrade')}")
        print(f"  Total Wallet : {info.get('totalWalletBalance')} USDT")
        print(f"  Avail Balance: {info.get('availableBalance')} USDT")
        print(f"  Total PnL    : {info.get('totalUnrealizedProfit')} USDT")
        assets = [a for a in info.get("assets", []) if float(a.get("walletBalance", 0)) > 0]
        if assets:
            print("\n  Non-zero asset balances:")
            for a in assets:
                print(f"    {a['asset']:10s}  wallet={a['walletBalance']}  available={a['availableBalance']}")
        print()
    except (BinanceAPIError, NetworkError) as e:
        print(f"❌  {e}\n")
        sys.exit(1)


def cmd_open_orders(args):
    client = get_client()
    symbol = args.symbol.upper() if args.symbol else None
    try:
        orders = client.get_open_orders(symbol=symbol)
        if not orders:
            print("\n  No open orders.\n")
            return
        print(f"\n── Open Orders ({len(orders)}) ──────────────────────────")
        for o in orders:
            print(
                f"  orderId={o['orderId']:>12}  {o['symbol']:10s}  "
                f"{o['side']:4s}  {o['type']:12s}  "
                f"qty={o['origQty']}  price={o.get('price', 'N/A')}  "
                f"status={o['status']}"
            )
        print()
    except (BinanceAPIError, NetworkError) as e:
        print(f"❌  {e}\n")
        sys.exit(1)


# ──────────────────────────────────────────────────────────────────────────────
# Parser definition
# ──────────────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Place a MARKET BUY
  python cli.py place --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  # Place a LIMIT SELL
  python cli.py place --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 70000

  # Place a STOP_MARKET BUY (bonus)
  python cli.py place --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.001 --stop-price 58000

  # Check account balance
  python cli.py account

  # List open orders
  python cli.py open-orders --symbol BTCUSDT
        """,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # ── place ──────────────────────────────────────────────────────────────
    place_p = sub.add_parser("place", help="Place an order on Binance Futures Testnet")
    place_p.add_argument("--symbol",     required=True,  help="Trading pair, e.g. BTCUSDT")
    place_p.add_argument("--side",       required=True,  choices=["BUY", "SELL"], help="Order side")
    place_p.add_argument("--type",       required=True,  choices=["MARKET", "LIMIT", "STOP_MARKET"],
                         dest="type",    help="Order type")
    place_p.add_argument("--quantity",   required=True,  type=float, help="Order quantity")
    place_p.add_argument("--price",      required=False, type=float, default=None,
                         help="Limit price (required for LIMIT orders)")
    place_p.add_argument("--stop-price", required=False, type=float, default=None, dest="stop_price",
                         help="Stop price (required for STOP_MARKET orders)")
    place_p.set_defaults(func=cmd_place)

    # ── account ────────────────────────────────────────────────────────────
    acc_p = sub.add_parser("account", help="Show account balance and info")
    acc_p.set_defaults(func=cmd_account)

    # ── open-orders ────────────────────────────────────────────────────────
    oo_p = sub.add_parser("open-orders", help="List open orders")
    oo_p.add_argument("--symbol", required=False, default=None, help="Filter by symbol")
    oo_p.set_defaults(func=cmd_open_orders)

    return parser


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

def main():
    log_file = setup_logging()
    import logging
    logging.getLogger(__name__).info("Trading bot started")
    print(f"\n📄 Logging to: {log_file}\n")

    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
