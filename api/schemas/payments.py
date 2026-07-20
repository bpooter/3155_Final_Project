from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from models.payments import PaymentType, TransactionStatus


class PaymentBase(BaseModel):
    order_id: int
    payment_type: PaymentType
    amount: Decimal
    transaction_status: TransactionStatus
    card_last_four: Optional[str] = None

class PaymentCreate(PaymentBase):
    order_id: int
    payment_type: PaymentType
    amount: Decimal
    card_last_four: Optional[str] = None

class PaymentUpdate(PaymentBase):
    payment_type: Optional[PaymentType] = None
    transaction_status: Optional[TransactionStatus] = None
    card_last_four: Optional[str] = None

class Payment(PaymentBase):
    payment_id: int

    class ConfigDict:
        from_attributes = True
