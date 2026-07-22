from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from .order_details import OrderDetail



class OrderBase(BaseModel):
    customer_id: Optional[int] = None
    guest_name: Optional[str] = None
    guest_email: Optional[str] = None
    guest_phone: Optional[str] = None
    promotion_code: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    guest_name: Optional[str] = None
    guest_email: Optional[str] = None
    guest_phone: Optional[str] = None
    order_status: Optional[str] = None
    promotion_code: Optional[str] = None

class Order(OrderBase):
    order_id: int
    customer_id: Optional[int] = None
    order_date: datetime
    order_status: str
    subtotal: Decimal
    discount_amount: Decimal
    total_price: Decimal
    order_details: list[OrderDetail] = Field(default_factory=list)

    class ConfigDict:
        from_attributes = True
