import pandas as pd
import numpy as np

def run_backtest(S1, S2, zscore, entry_threshold=2.0, exit_threshold=0.0):
    """
    Simulates trades based on z-score thresholds.
    """
    signals = pd.DataFrame(index=zscore.index)
    signals['zscore'] = zscore

    # Simple simulation logic
    pos = 0
    positions = []

    for i in range(len(zscore)):
        z = zscore.iloc[i]
        if np.isnan(z):
            positions.append(0)
            continue

        if z < -entry_threshold:
            pos = 1 # Long spread -> Long S2, Short S1
        elif z > entry_threshold:
            pos = -1 # Short spread -> Short S2, Long S1
        elif (pos == 1 and z >= -exit_threshold) or (pos == -1 and z <= exit_threshold):
            pos = 0

        positions.append(pos)

    signals['position'] = positions
    return signals

def calculate_returns(signals, S1, S2, hedge_ratio):
    """
    Calculates returns for the backtest.
    """
    delta_S1 = S1.diff()
    delta_S2 = S2.diff()

    # Daily profit/loss per unit of the spread
    daily_pnl = signals['position'].shift(1) * (delta_S2 - hedge_ratio * delta_S1)

    # Capital requirement (approximate: value of both legs)
    capital = S2 + hedge_ratio * S1

    signals['returns'] = daily_pnl / capital
    signals['cumulative_returns'] = (1 + signals['returns'].fillna(0)).cumprod()
    return signals
