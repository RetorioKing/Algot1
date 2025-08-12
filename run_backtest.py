import os, yaml, pandas as pd
from datetime import datetime
from growwapi import GrowwAPI
from .engine import fetch_ohlc
from ..strategies.equity_vwap_reversion import generate_signals as vwap_signal
from ..strategies.index_trend import generate_signals as trend_signal
def run():
    token=os.getenv("GROWW_ACCESS_TOKEN")
    if not token and not os.getenv("GROWW_API_KEY"): raise SystemExit("Set Groww credentials in .env")
    if token: g=GrowwAPI(token)
    else:
        import pyotp
        key=os.getenv("GROWW_API_KEY"); secret=os.getenv("GROWW_API_SECRET")
        g=GrowwAPI(GrowwAPI.get_access_token(key, pyotp.TOTP(secret).now()))
    start=datetime.fromisoformat(os.getenv("BT_START","2025-07-11 09:15:00"))
    end  =datetime.fromisoformat(os.getenv("BT_END","2025-08-11 15:20:00"))
    # Example: RELIANCE equity intraday (VWAP reversion)
    eq = fetch_ohlc(g,"RELIANCE","NSE","CASH",start,end,1)
    print("Equity minute bars:", len(eq))
    # Example: Index future symbol placeholder; replace with current front symbol
    fut = fetch_ohlc(g,"NIFTY25AUGFUT","NSE","FNO",start,end,1)
    print("Index future minute bars:", len(fut))
if __name__=="__main__": run()
