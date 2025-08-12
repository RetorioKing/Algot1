import pandas as pd, pandas_ta as ta
def generate_signals(df: pd.DataFrame, rsi_len=5, rsi_low=20, rsi_high=80, vwap_sigma_mult=1.2):
    if len(df) < 50: return {"side": None}
    vwap = ta.vwap(df['high'], df['low'], df['close'], df['volume']); rsi = ta.rsi(df['close'], length=rsi_len)
    sigma = df['close'].rolling(30).std()
    below = (df['close'].iloc[-1] < vwap.iloc[-1] - vwap_sigma_mult * sigma.iloc[-1]) and (rsi.iloc[-1] < rsi_low)
    above = (df['close'].iloc[-1] > vwap.iloc[-1] + vwap_sigma_mult * sigma.iloc[-1]) and (rsi.iloc[-1] > rsi_high)
    if below: return {"side":"BUY"}
    if above: return {"side":"SELL"}
    return {"side": None}
