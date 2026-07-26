from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from .sandwiches import Sandwich



class OrderDetailBase(BaseModel):
    order_id: int
    menu_item_id: int
    quantity: int = Field(gt=0)
    special_instructions: Optional[str] = None


class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetailUpdate(BaseModel):
    quantity: Optional[int] = None
    special_instructions: Optional[str] = None


class OrderDetail(OrderDetailBase):
    order_detail_id: int
    unit_price: Decimal

    class ConfigDict:
        from_attributes = True