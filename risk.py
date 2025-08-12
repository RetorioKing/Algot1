from dataclasses import dataclass
from .logger import get_logger
LOG = get_logger("Risk")
@dataclass
class RiskConfig:
    per_trade_risk_pct: float
    daily_max_loss_pct: float
    max_open_positions: int
    notional_cap_per_trade: float
class RiskManager:
    def __init__(self, cfg: RiskConfig):
        self.cfg = cfg; self.day_pnl = 0.0; self.trades_open = 0; self.killed = False
    def can_open(self, equity: float, est_loss: float) -> bool:
        if self.killed or self.trades_open >= self.cfg.max_open_positions: return False
        if abs(self.day_pnl) >= equity * self.cfg.daily_max_loss_pct: LOG.warning("Daily loss hit; kill-switch"); self.killed=True; return False
        return est_loss <= equity * self.cfg.per_trade_risk_pct
    def on_open(self): self.trades_open += 1
    def on_close(self, pnl: float): self.trades_open = max(0, self.trades_open - 1); self.day_pnl += pnl
