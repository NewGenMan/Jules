import time
import datetime
from src.data_loader import YFinanceDataLoader, get_closing_prices
from src.strategy import calculate_spread, calculate_zscore
from src.pair_finder import calculate_hedge_ratio
from src.broker import MockBroker

def live_trading_loop(stock1, stock2, broker, interval='5m', window=20, entry_threshold=2.0, exit_threshold=0.0):
    """
    Simulates a live trading loop.
    In a real system, this would run indefinitely or during market hours.
    """
    print(f"Starting live trading loop for {stock1} and {stock2}...")
    data_loader = YFinanceDataLoader()

    # Initial setup: Calculate hedge ratio from historical data
    end_dt = datetime.datetime.now()
    start_dt = end_dt - datetime.timedelta(days=30)

    print("Calculating historical hedge ratio...")
    hist_data = data_loader.download_data([stock1, stock2], start_dt.strftime('%Y-%m-%d'), end_dt.strftime('%Y-%m-%d'), interval=interval)
    prices = get_closing_prices(hist_data)
    hedge_ratio = calculate_hedge_ratio(prices[stock1], prices[stock2])
    print(f"Hedge Ratio: {hedge_ratio:.4f}")

    current_pos = 0 # 1 for Long S2/Short S1, -1 for Short S2/Long S1, 0 for Flat

    # Simulation of 5 iterations
    for i in range(5):
        print(f"\n--- Iteration {i+1} ---")

        # 1. Fetch latest data
        latest_data = data_loader.download_data([stock1, stock2],
                                                (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                                                datetime.datetime.now().strftime('%Y-%m-%d'),
                                                interval=interval)
        prices = get_closing_prices(latest_data)

        # 2. Calculate Z-Score
        spread = calculate_spread(prices[stock1], prices[stock2], hedge_ratio)
        zscore = calculate_zscore(spread, window).iloc[-1]
        print(f"Current Z-Score: {zscore:.4f}")

        # 3. Execution Logic
        if zscore < -entry_threshold and current_pos != 1:
            print("SIGNAL: Long Spread (Buy S2, Sell S1)")
            broker.place_order(stock2, 100, 'BUY')
            broker.place_order(stock1, int(100 * hedge_ratio), 'SELL')
            current_pos = 1
        elif zscore > entry_threshold and current_pos != -1:
            print("SIGNAL: Short Spread (Sell S2, Buy S1)")
            broker.place_order(stock2, 100, 'SELL')
            broker.place_order(stock1, int(100 * hedge_ratio), 'BUY')
            current_pos = -1
        elif abs(zscore) < exit_threshold and current_pos != 0:
            print("SIGNAL: Exit Position")
            if current_pos == 1:
                broker.place_order(stock2, 100, 'SELL')
                broker.place_order(stock1, int(100 * hedge_ratio), 'BUY')
            else:
                broker.place_order(stock2, 100, 'BUY')
                broker.place_order(stock1, int(100 * hedge_ratio), 'SELL')
            current_pos = 0
        else:
            print("No action taken.")

        # Wait for next bar (simulated)
        # time.sleep(300) # 5 minutes

    print("\nLive trading simulation complete.")

if __name__ == "__main__":
    broker = MockBroker()
    live_trading_loop('SPY', 'IVV', broker)
