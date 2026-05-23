# Simons Scalping System

A systematic US stock market scalping system based on Jim Simons' statistical arbitrage and mean reversion principles.

## Features
- **Purely Systematic**: Automated logic for data fetching, pair selection, and trading signals.
- **Statistical Arbitrage**: Identifies cointegrated pairs (e.g., SPY/IVV, AAPL/MSFT) using Engle-Granger tests.
- **High-Frequency Scalping**: Backtester configured for 5-minute intraday intervals.
- **Mean Reversion Strategy**: Generates trades based on z-score deviations of the price spread.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the System

### 1. Run the Backtester
To find cointegrated pairs and run a backtest on recent 5-minute data:

**On Linux/macOS:**
```bash
python run_system.py
```

**On Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "."
python run_system.py
```

This will:
- Download recent intraday data for a set of tickers.
- Identify pairs that are statistically cointegrated.
- Run a backtest on the best pair found.
- Save the results to `backtest_results.csv`.

### 2. Run the Dashboard (UI)
To visualize the strategy and monitor results in a web interface:

**On Linux/macOS:**
```bash
python run_dashboard.py
```

**On Windows (PowerShell):**
```powershell
python run_dashboard.py
```

### 3. Run Unit Tests
To verify the core mathematical logic:

**On Linux/macOS:**
```bash
pytest
```

**On Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "."
pytest
```

## TradingView Integration

Connecting with TradingView Desktop directly for live data capture is best achieved via two primary methods:

### 1. Programmatic Access (tvDatafeed)
You can use the `tvDatafeed` library to scrape data directly from TradingView's servers.
- **Pros**: Access to all symbols and intervals available on TV.
- **Setup**: `pip install --upgrade --no-cache-dir git+https://github.com/rongardF/tvdatafeed.git`

### 2. Live Alerts via Webhooks (Recommended for Execution)
To capture real-time signals or price data from a TradingView Desktop chart:
- **Alerts**: Create an alert on TradingView using your strategy/indicator.
- **Webhook**: Set the Alert Action to "Webhook URL" and point it to a local/cloud server (e.g., using Flask or FastAPI).
- **Processing**: The system can listen for these POST requests to trigger scalping trades instantaneously.

## System Principles (AGENTS.md)
The system strictly follows these rules:
1. **Never override the computer.**
2. **Capitalize on mean reversion.**
3. **Target small, high-frequency edges.**
4. **Constantly evolve and re-test.**
