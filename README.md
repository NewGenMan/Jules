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
```bash
export PYTHONPATH=$PYTHONPATH:.
python src/main.py
```
This will:
- Download recent intraday data for a set of tickers.
- Identify pairs that are statistically cointegrated.
- Run a backtest on the best pair found.
- Save the results to `backtest_results.csv`.

### 2. Run Unit Tests
To verify the core mathematical logic:
```bash
export PYTHONPATH=$PYTHONPATH:.
pytest tests/
```

## System Principles (AGENTS.md)
The system strictly follows these rules:
1. **Never override the computer.**
2. **Capitalize on mean reversion.**
3. **Target small, high-frequency edges.**
4. **Constantly evolve and re-test.**
