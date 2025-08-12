import time, pandas as pd
from datetime import datetime, timedelta
from growwapi import GrowwAPI
def daterange_chunks(start, end, interval_min):
    if interval_min==1: window=timedelta(days=7)
    elif interval_min==5: window=timedelta(days=15)
    elif interval_min==10: window=timedelta(days=30)
    elif interval_min==60: window=timedelta(days=150)
    else: window=timedelta(days=7)
    cur=start; chunks=[]
    while cur<end:
        nxt=min(end, cur+window); chunks.append((cur,nxt)); cur=nxt+timedelta(minutes=interval_min)
    return chunks
def fetch_ohlc(g: GrowwAPI, trading_symbol, exchange, segment, start, end, interval_min):
    rows=[]
    for s,e in daterange_chunks(start,end,interval_min):
        resp = g.get_historical_candle_data(trading_symbol=trading_symbol, exchange=getattr(g,f"EXCHANGE_{exchange}"),
                  segment=getattr(g,f"SEGMENT_{segment}"), start_time=s.strftime("%Y-%m-%d %H:%M:%S"),
                  end_time=e.strftime("%Y-%m-%d %H:%M:%S"), interval_in_minutes=interval_min)
        for t,o,h,l,c,v in resp.get("candles",[]):
            rows.append((pd.to_datetime(t, unit="s"), o,h,l,c,v))
        time.sleep(0.1)
    if not rows: return pd.DataFrame(columns=["ts","open","high","low","close","volume"]).set_index("ts")
    df = pd.DataFrame(rows, columns=["ts","open","high","low","close","volume"]).drop_duplicates("ts").sort_values("ts").set_index("ts")
    return df
