import pytest
import pandas as pd
import numpy as np
from src.strategy import calculate_spread, calculate_zscore
from src.pair_finder import calculate_hedge_ratio

def test_calculate_spread():
    S1 = pd.Series([10, 11, 10, 11])
    S2 = pd.Series([20, 22, 20, 22])
    hedge_ratio = 2.0
    spread = calculate_spread(S1, S2, hedge_ratio)
    assert (spread == 0).all()

def test_calculate_zscore():
    spread = pd.Series([1, 1, 1, 1, 1, 1, 1, 1, 1, 10])
    zscore = calculate_zscore(spread, window=5)
    assert not np.isnan(zscore.iloc[-1])
    assert zscore.iloc[-1] > 0

def test_calculate_hedge_ratio():
    S1 = pd.Series([1, 2, 3, 4, 5])
    S2 = pd.Series([2, 4, 6, 8, 10])
    ratio = calculate_hedge_ratio(S1, S2)
    assert np.isclose(ratio, 2.0)
