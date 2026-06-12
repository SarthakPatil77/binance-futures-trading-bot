# Binance Futures Testnet Trading Bot

A clean, modular Python CLI application for placing and managing orders on the Binance Futures Testnet (USDT-M). The project demonstrates structured software design, input validation, logging, error handling, and Binance API integration.

---

## Overview

This trading bot allows users to:

* Place MARKET orders
* Place LIMIT orders
* Place STOP_MARKET orders (Bonus)
* Support BUY and SELL order sides
* View Futures account information
* List open orders
* Validate user inputs before API requests
* Log API requests, responses, and errors
* Handle API and network failures gracefully

The application is built using a layered architecture that separates API communication, business logic, validation, and CLI functionality.

---

## Project Structure

```text
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
│
├── logs/
│   ├── market_order_sample.log
│   └── limit_order_sample.log
│
├── cli.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Module Description

| File              | Purpose                  |
| ----------------- | ------------------------ |
| client.py         | Binance REST API wrapper |
| orders.py         | Order placement logic    |
| validators.py     | Input validation         |
| logging_config.py | Logging setup            |
| cli.py            | Command-line interface   |

---

## Requirements

* Python 3.9+
* Binance Futures Testnet Account
* Binance Futures Testnet API Key
* Internet Connection

---

## Binance Futures Testnet Setup

### Create Testnet Account

1. Visit https://testnet.binancefuture.com
2. Login using GitHub or Binance credentials
3. Open API Management
4. Generate API Key and Secret Key
5. Save the credentials securely

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd trading_bot
```

### Create Virtual Environment

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

### Linux/macOS

```bash
export BINANCE_API_KEY="your_api_key"
export BINANCE_API_SECRET="your_secret_key"
```

### Windows PowerShell

```powershell
$env:BINANCE_API_KEY="your_api_key"
$env:BINANCE_API_SECRET="your_secret_key"
```

Verify:

```powershell
echo $env:BINANCE_API_KEY
```

---

## Usage

All commands are executed from the project root directory.

---

### Account Information

```bash
python cli.py account
```

Example Output:

```text
Account Info

Can Trade       : True
Total Wallet    : 5000.00000000 USDT
Available Bal   : 5000.00000000 USDT
Total PnL       : 0.00000000 USDT
```

---

### MARKET Order

Buy BTC at market price:

```bash
python cli.py place --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

Sell BTC at market price:

```bash
python cli.py place --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

---

### LIMIT Order

Buy BTC at a specific price:

```bash
python cli.py place --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 100000
```

Sell BTC at a specific price:

```bash
python cli.py place --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 120000
```

---

### STOP_MARKET Order (Bonus)

```bash
python cli.py place --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.001 --stop-price 58000
```

---

### Open Orders

List orders for BTCUSDT:

```bash
python cli.py open-orders --symbol BTCUSDT
```

List all open orders:

```bash
python cli.py open-orders
```

---

## Sample Output

```text
ORDER REQUEST

Symbol      : BTCUSDT
Side        : BUY
Type        : MARKET
Quantity    : 0.001

ORDER RESPONSE

Order ID      : 123456789
Symbol        : BTCUSDT
Status        : FILLED
Executed Qty  : 0.001
Avg Price     : 107500.00

SUCCESS: MARKET order placed successfully
```

---

## Logging

The application creates timestamped log files under the logs directory.

### Logging Features

* Request logging
* Response logging
* Validation logging
* Error logging
* Network exception logging

Example:

```text
2026-06-12 10:45:12 | INFO | bot.orders | Placing MARKET order
2026-06-12 10:45:12 | DEBUG | bot.client | REQUEST POST /fapi/v1/order
2026-06-12 10:45:12 | DEBUG | bot.client | RESPONSE HTTP 200
2026-06-12 10:45:12 | INFO | bot.orders | Order successful
```

---

## Error Handling

The application handles:

### Missing Credentials

```text
Missing BINANCE_API_KEY or BINANCE_API_SECRET
```

### Validation Errors

```text
LIMIT orders require --price
```

### Binance API Errors

```text
Binance API Error -2015:
Invalid API-key, IP, or permissions for action
```

### Network Errors

```text
Connection timeout
Unable to reach Binance Futures Testnet
```

---

## Assumptions

* Binance USDT-M Futures Testnet only
* LIMIT orders use GTC (Good Till Cancelled)
* API credentials supplied through environment variables
* No leverage configuration included
* No position management included
* Educational/Testnet use only

---

## Bonus Features Implemented

* STOP_MARKET order support
* Account information command
* Open orders command
* Enhanced validation messages
* Structured logging
* Modular architecture

---

## Assignment Requirements Checklist

### Core Requirements

* Python 3.x
* Binance Futures Testnet Integration
* MARKET Orders
* LIMIT Orders
* BUY Support
* SELL Support
* CLI Interface
* Input Validation
* Structured Logging
* Exception Handling
* Order Summary Output
* Order Response Output

### Deliverables

* Source Code
* README.md
* requirements.txt
* Log Files
* Public GitHub Repository

---

## Author

Sarthak Patil

