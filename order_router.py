from dataclasses import dataclass
from ..core.logger import get_logger
from ..core.utils import ref_id
from ..core.groww_broker import GrowwBroker
LOG = get_logger("OrderRouter")
@dataclass
class OrderRequest:
    symbol: str; segment: str; exchange: str; product: str; side: str; order_type: str; qty: int
    price: float | None = None; trigger_price: float | None = None; strategy: str = "default"
class OrderRouter:
    def __init__(self, broker: GrowwBroker): self.b = broker; self.serial = 0
    def place(self, req: OrderRequest):
        self.serial += 1; rid = ref_id(req.strategy, self.serial)
        LOG.info(f"Placing {req.side} {req.qty} {req.symbol} [{req.segment}/{req.product}] ref={rid}")
        return self.b.place_order(trading_symbol=req.symbol, quantity=req.qty, validity=self.b.g.VALIDITY_DAY,
            exchange=self.b.g.EXCHANGE_NSE if req.exchange=='NSE' else self.b.g.EXCHANGE_BSE,
            segment=self.b.g.SEGMENT_FNO if req.segment=='FNO' else self.b.g.SEGMENT_CASH,
            product=getattr(self.b.g, f'PRODUCT_{req.product}'), order_type=getattr(self.b.g, f'ORDER_TYPE_{req.order_type}'),
            transaction_type=getattr(self.b.g, f'TRANSACTION_TYPE_{req.side}'), price=req.price, trigger_price=req.trigger_price,
            order_reference_id=rid)
