# Binance Futures Testnet Trading Bot

A clean, well-structured Python CLI application for placing orders on the **Binance Futures Testnet (USDT-M)**. Built with a layered architecture separating the API client, order logic, validation, and CLI — with structured logging and robust error handling throughout.

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance REST client (auth, signing, request dispatch)
│   ├── orders.py          # Order placement logic (MARKET, LIMIT, STOP_MARKET)
│   ├── validators.py      # Input validation with descriptive errors
│   └── logging_config.py  # File + console logging setup
├── cli.py                 # CLI entry point (argparse)
├── logs/                  # Auto-created; log files written here
│   ├── market_order_sample.log
│   └── limit_order_sample.log
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Get Binance Futures Testnet credentials

1. Visit [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Log in with a GitHub account
3. Go to **API Key** tab → generate a key pair
4. Copy your **API Key** and **Secret Key**

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set environment variables

```bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_api_secret_here"
```

On Windows (PowerShell):
```powershell
$env:BINANCE_API_KEY = "your_api_key_here"
$env:BINANCE_API_SECRET = "your_api_secret_here"
```

---

## Usage

All commands are run from the `trading_bot/` directory.

### Place a MARKET order

```bash
# Buy 0.001 BTC at market price
python cli.py place --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Sell 0.01 ETH at market price
python cli.py place --symbol ETHUSDT --side SELL --type MARKET --quantity 0.01
```

### Place a LIMIT order

```bash
# Sell 0.001 BTC at $70,000
python cli.py place --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 70000

# Buy 0.01 ETH at $2,500
python cli.py place --symbol ETHUSDT --side BUY --type LIMIT --quantity 0.01 --price 2500
```

### Place a STOP_MARKET order (Bonus)

```bash
# Trigger a market BUY if BTC drops to $58,000
python cli.py place --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.001 --stop-price 58000
```

### Check account balance

```bash
python cli.py account
```

### List open orders

```bash
python cli.py open-orders --symbol BTCUSDT
python cli.py open-orders          # all symbols
```

---

## Example Output

```
📄 Logging to: logs/trading_bot_20260611_101201.log

┌─────────────── ORDER REQUEST ───────────────┐
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.001
└─────────────────────────────────────────────┘
┌─────────────── ORDER RESPONSE ──────────────┐
  Order ID       : 4751823
  Client OID     : web_1749632521000
  Symbol         : BTCUSDT
  Side           : BUY
  Type           : MARKET
  Status         : FILLED
  Executed Qty   : 0.001
  Avg Price      : 67341.20
└─────────────────────────────────────────────┘
✅  MARKET order placed successfully!
```

---

## Logging

Each run creates a timestamped log file under `logs/`. Both file and console handlers are active:

- **Console**: INFO level and above
- **File**: DEBUG level (full request/response details, validation steps)

Log format:
```
2026-06-11 10:12:01 | INFO     | bot.orders | Placing MARKET order: BUY 0.001 BTCUSDT
2026-06-11 10:12:01 | DEBUG    | bot.client | → POST .../fapi/v1/order | params: {...}
2026-06-11 10:12:01 | DEBUG    | bot.client | ← HTTP 200 | body: {...}
2026-06-11 10:12:01 | INFO     | bot.orders | MARKET order success: orderId=4751823, status=FILLED
```

---

## Error Handling

| Scenario | Behaviour |
|---|---|
| Missing API keys | Clear message + `sys.exit(1)` |
| Invalid symbol/side/type | `ValidationError` with descriptive message |
| Missing price for LIMIT | Caught before API call |
| Binance API error (4xx) | Parsed error code + message printed |
| Network timeout / connection refused | `NetworkError` with guidance |

---

## Assumptions

- Uses **USDT-M Futures Testnet** only (`https://testnet.binancefuture.com`)
- LIMIT orders use `timeInForce=GTC` (Good Till Cancelled) by default
- STOP_MARKET uses `CONTRACT_PRICE` working type (Binance default)
- Credentials are passed via environment variables (not hardcoded or in config files)
- No position management or leverage configuration — pure order placement

---

## Bonus Features Implemented

- **STOP_MARKET order type** — triggers a market order when a stop price is hit
- **`account` command** — shows wallet balance and unrealised PnL
- **`open-orders` command** — lists all open orders with optional symbol filter
