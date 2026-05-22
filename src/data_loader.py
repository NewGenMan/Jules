import yfinance as yf
import pandas as pd
import os

def download_data(tickers, start_date, end_date, interval='1d', data_dir='data'):
    """
    Downloads historical data for a list of tickers.
    """
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    data = {}
    for ticker in tickers:
        file_path = os.path.join(data_dir, f"{ticker}_{interval}.csv")
        if os.path.exists(file_path):
            print(f"Loading {ticker} from {file_path}")
            df = pd.read_csv(file_path, index_col=0, header=[0, 1], parse_dates=True)
            # Flatten multi-index columns if necessary
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

def get_closing_prices(data_dict):
    """
    Extracts 'Close' prices from a dictionary of dataframes and joins them.
    """
    closing_prices = pd.DataFrame()
    for ticker, df in data_dict.items():
        if not df.empty:
            closing_prices[ticker] = df['Close']
    return closing_prices.dropna()
