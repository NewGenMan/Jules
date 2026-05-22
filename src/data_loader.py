import yfinance as yf
import pandas as pd
import os

class DataLoader:
    """Base class for data loaders."""
    def download_data(self, tickers, start_date, end_date, interval='1d'):
        raise NotImplementedError

class YFinanceDataLoader(DataLoader):
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def download_data(self, tickers, start_date, end_date, interval='1d'):
        data = {}
        for ticker in tickers:
            file_path = os.path.join(self.data_dir, f"{ticker}_{interval}.csv")
            if os.path.exists(file_path):
                print(f"Loading {ticker} from {file_path}")
                # yfinance often saves with a 2-row header (Price, Ticker)
                # We try to detect if we need to skip a row or use MultiIndex
                df = pd.read_csv(file_path, index_col=0, header=[0, 1], parse_dates=True)
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
            else:
                print(f"Downloading {ticker}...")
                df = yf.download(ticker, start=start_date, end=end_date, interval=interval)
                if not df.empty:
                    df.to_csv(file_path)
                else:
                    print(f"Warning: No data for {ticker}")
            data[ticker] = df
        return data

class TradingViewDataLoader(DataLoader):
    """
    Placeholder for TradingView data capture.
    Could be implemented using tvDatafeed or a local Webhook server.
    """
    def download_data(self, tickers, start_date, end_date, interval='1d'):
        print("TradingView data capture not yet implemented.")
        return {}

def get_closing_prices(data_dict):
    """Extracts 'Close' prices and joins them."""
    closing_prices = pd.DataFrame()
    for ticker, df in data_dict.items():
        if not df.empty:
            closing_prices[ticker] = df['Close']
    return closing_prices.dropna()

# Backward compatibility
def download_data(tickers, start_date, end_date, interval='1d', data_dir='data'):
    loader = YFinanceDataLoader(data_dir)
    return loader.download_data(tickers, start_date, end_date, interval)
