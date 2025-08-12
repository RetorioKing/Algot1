import numpy as np, pandas as pd
def sharpe(series, risk_free=0.0, periods_per_year=252):
    r = series.dropna()
    if len(r) < 2: return np.nan
    excess = r - risk_free/periods_per_year
    ann = np.sqrt(periods_per_year) * (excess.mean() / (excess.std(ddof=1)+1e-12))
    return float(ann)
def max_drawdown(cum):
    roll_max = cum.cummax(); dd = cum/roll_max - 1.0
    end = dd.idxmin(); 
    if pd.isna(end): return 0.0, None, None
    start = (cum.loc[:end]).idxmax(); 
    return float(dd.min()), start, end
def profit_factor(pnl_by_trade: pd.Series):
    gains = pnl_by_trade[pnl_by_trade>0].sum(); losses = -pnl_by_trade[pnl_by_trade<0].sum()
    return float(np.inf if losses==0 else gains/max(losses,1e-12))
