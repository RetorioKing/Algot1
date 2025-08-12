import time, random, string
from datetime import datetime, timedelta, timezone
IST = timezone(timedelta(hours=5, minutes=30))
def now_ist(): return datetime.now(tz=IST)
def jitter_sleep(base=0.12, jitter=0.05): time.sleep(max(0.0, base + random.uniform(-jitter, jitter)))
def ref_id(strategy: str, seq: int):
    today = now_ist().strftime("%Y%m%d")
    return f"{strategy}-{today}-{seq:04d}-" + "".join(random.choices(string.ascii_uppercase+string.digits, k=4))
