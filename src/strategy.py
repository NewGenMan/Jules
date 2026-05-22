import pandas as pd
import numpy as np

def calculate_spread(S1, S2, hedge_ratio):
    """
    Calculates the spread between two series.
    """
    return S2 - hedge_ratio * S1

def calculate_zscore(spread, window):
    """
    Calculates the z-score of the spread.
    """
    mean = spread.rolling(window=window).mean()
    std = spread.rolling(window=window).std()
    zscore = (spread - mean) / std
    return zscore
