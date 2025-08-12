import pandas as pd, pandas_ta as ta
def generate_signals(df: pd.DataFrame, ema_fast=20, ema_slow=50, adx_len=14, adx_min=20):
    if len(df) < max(ema_slow, adx_len) + 2: return {"side": None}
    ema_f, ema_s = ta.ema(df['close'], length=ema_fast), ta.ema(df['close'], length=ema_slow)
    adx = ta.adx(df['high'], df['low'], df['close'], length=adx_len)['ADX_'+str(adx_len)]
    if ema_f.iloc[-1] > ema_s.iloc[-1] and adx.iloc[-1] >= adx_min: return {"side":"BUY"}
    if ema_f.iloc[-1] < ema_s.iloc[-1] and adx.iloc[-1] >= adx_min: return {"side":"SELL"}
    return {"side": None}
