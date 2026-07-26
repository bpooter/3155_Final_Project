from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from ..models.payments import PaymentType, TransactionStatus


class PaymentBase(BaseModel):
    order_id: int
    payment_type: PaymentType
    amount: Decimal = Field(gt=0)
    transaction_status: TransactionStatus
    card_last_four: Optional[str] = Field(default=None, min_length=4, max_length=4)

class PaymentCreate(PaymentBase):
    order_id: int
    payment_type: PaymentType
    amount: Decimal = Field(gt=0)
    card_last_four: Optional[str] = Field(default=None, min_length=4, max_length=4)

class PaymentUpdate(BaseModel):
    payment_type: Optional[PaymentType] = None
    amount: Optional[Decimal] = Field(default=None, gt=0)
    transaction_status: Optional[TransactionStatus] = None
    card_last_four: Optional[str] = Field(default=None, min_length=4, max_length=4)

class Payment(PaymentBase):
    payment_id: int

    class ConfigDict:
        from_attributes = True
