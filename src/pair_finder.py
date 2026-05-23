import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm

def find_cointegrated_pairs(data):
    """
    Finds pairs of stocks that are cointegrated.
    """
    n = data.shape[1]
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            S1 = data[keys[i]]
            S2 = data[keys[j]]
            result = coint(S1, S2)
            score = result[0]
            pvalue = result[1]
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            if pvalue < 0.05:
                pairs.append((keys[i], keys[j], pvalue))
    return score_matrix, pvalue_matrix, pairs

def calculate_hedge_ratio(S1, S2):
    """
    Calculates the hedge ratio using OLS.
    """
    S1_with_const = sm.add_constant(S1)
    results = sm.OLS(S2, S1_with_const).fit()
    # If S1 was a Series named 'Symbol', params might have 'Symbol' as index
    # instead of 1. Using iloc is safer if we want the second parameter.
    return results.params.iloc[1]
