import matplotlib.pyplot as plt
from src.data_loader import download_data, get_closing_prices
from src.pair_finder import find_cointegrated_pairs, calculate_hedge_ratio
from src.strategy import calculate_spread, calculate_zscore
from src.backtester import run_backtest, calculate_returns
import os

def main():
    # 1. Download Data
    # For scalping/high-frequency, we use '5m' interval
    # Note: yfinance 5m data is only available for the last 60 days.
    # Using a relative range would be better but for this demo we'll use
    # very recent dates. Assuming today is mid-March 2025.
    tickers = ['SPY', 'IVV', 'GLD', 'GDX', 'AAPL', 'MSFT', 'META', 'GOOGL']
    import datetime
    end_dt = datetime.datetime.now()
    start_dt = end_dt - datetime.timedelta(days=59)

    start_date = start_dt.strftime('%Y-%m-%d')
    end_date = end_dt.strftime('%Y-%m-%d')
    interval = '5m'

    print(f"Downloading data with interval {interval}...")
    data_dict = download_data(tickers, start_date, end_date, interval=interval)
    closing_prices = get_closing_prices(data_dict)

    # 2. Find Cointegrated Pairs
    print("Finding cointegrated pairs...")
    scores, pvalues, pairs = find_cointegrated_pairs(closing_prices)
    print(f"Found {len(pairs)} cointegrated pairs.")
    for p in pairs:
        print(f"Pair: {p[0]} - {p[1]}, P-value: {p[2]:.4f}")

    if not pairs:
        print("No cointegrated pairs found. Exiting.")
        return

    # 3. Backtest the first pair
    stock1, stock2, _ = pairs[0]
    print(f"Backtesting pair: {stock1}, {stock2}")

    S1 = closing_prices[stock1]
    S2 = closing_prices[stock2]

    hedge_ratio = calculate_hedge_ratio(S1, S2)
    print(f"Hedge Ratio: {hedge_ratio:.4f}")

    spread = calculate_spread(S1, S2, hedge_ratio)
    zscore = calculate_zscore(spread, window=20)

    signals = run_backtest(S1, S2, zscore)
    results = calculate_returns(signals, S1, S2, hedge_ratio)

    print(f"Final Cumulative Return: {results['cumulative_returns'].iloc[-1]:.4f}")

    # 4. Save results
    results.to_csv('backtest_results.csv')
    print("Results saved to backtest_results.csv")

if __name__ == "__main__":
    main()
