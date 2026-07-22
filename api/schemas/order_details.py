from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from .sandwiches import Sandwich

'''
id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10,2), nullable=False)
    special_instructions = Column(String(255), nullable=True)
    sandwich = relationship("Sandwich", back_populates="order_details")
    order = relationship("Order", back_populates="order_details")

'''


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