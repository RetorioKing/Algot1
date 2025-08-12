from datetime import datetime, time as dtime, timedelta, timezone
IST = timezone(timedelta(hours=5, minutes=30))
def is_market_open(now: datetime, open_str: str, close_str: str, skip_first_min: int, skip_last_min: int):
    o,c = dtime.fromisoformat(open_str), dtime.fromisoformat(close_str)
    start = now.replace(hour=o.hour, minute=o.minute, second=0, microsecond=0)+timedelta(minutes=skip_first_min)
    end = now.replace(hour=c.hour, minute=c.minute, second=0, microsecond=0)-timedelta(minutes=skip_last_min)
    return start <= now <= end
def squareoff_due(now: datetime, squareoff_str: str):
    s = dtime.fromisoformat(squareoff_str); at = now.replace(hour=s.hour, minute=s.minute, second=0, microsecond=0)
    return now >= at
