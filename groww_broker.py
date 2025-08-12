from growwapi import GrowwAPI
import pyotp, os
from .logger import get_logger
from .utils import jitter_sleep
LOG = get_logger("GrowwBroker")
class GrowwBroker:
    def __init__(self):
        access_token = os.getenv("GROWW_ACCESS_TOKEN")
        api_key, api_secret = os.getenv("GROWW_API_KEY"), os.getenv("GROWW_API_SECRET")
        if access_token:
            LOG.info("Auth via Access Token"); self.g = GrowwAPI(access_token)
        elif api_key and api_secret:
            LOG.info("Auth via TOTP"); tok = GrowwAPI.get_access_token(api_key, pyotp.TOTP(api_secret).now()); self.g = GrowwAPI(tok)
        else: raise RuntimeError("Set GROWW_ACCESS_TOKEN or GROWW_API_KEY + GROWW_API_SECRET")
        self.ops_delay = 0.12
    def _t(self): jitter_sleep(self.ops_delay, 0.02)
    def place_order(self, **k): self._t(); return self.g.place_order(**k)
    def modify_order(self, **k): self._t(); return self.g.modify_order(**k)
    def cancel_order(self, **k): self._t(); return self.g.cancel_order(**k)
    def get_positions(self, **k): return self.g.get_positions_for_user(**k)
    def get_holdings(self, **k): return self.g.get_holdings_for_user(**k)
    def get_margin(self, **k): return self.g.get_margin_detail_for_user(**k)
    def quote(self, exchange, segment, trading_symbol): return self.g.get_quote(exchange=exchange, segment=segment, trading_symbol=trading_symbol)
    def ltp(self, segment, exchange_trading_symbols): return self.g.get_ltp(segment=segment, exchange_trading_symbols=exchange_trading_symbols)
