import os, time, yaml, threading
from core.logger import get_logger
from core.utils import now_ist
from core.clock import is_market_open, squareoff_due
from core.groww_broker import GrowwBroker
from execution.order_router import OrderRouter
LOG = get_logger("Main")
def run_api():
    import uvicorn; from api.app import app
    uvicorn.run(app, host="0.0.0.0", port=8088, log_level="info")
def main():
    cfg = yaml.safe_load(open("config.yml"))
    run_mode = os.getenv("RUN_MODE","paper"); LOG.info(f"RUN_MODE={run_mode}")
    broker = GrowwBroker(); router = OrderRouter(broker)
    threading.Thread(target=run_api, daemon=True).start()
    while True:
        now = now_ist()
        if squareoff_due(now, cfg["market"]["auto_squareoff_time"]): LOG.warning("Square-off due — flatten here"); time.sleep(60); continue
        if not is_market_open(now, cfg["market"]["ist_open"], cfg["market"]["ist_close"], cfg["market"]["skip_first_minutes"], cfg["market"]["skip_last_minutes"]):
            time.sleep(5); continue
        # TODO: Build bars, run strategies, size, route orders
        time.sleep(1)
if __name__ == "__main__": main()
