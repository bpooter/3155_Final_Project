from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class OrderDetail(Base):
    __tablename__ = "order_details"

    order_detail_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.menu_item_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10,2), nullable=False)
    special_instructions = Column(String(255), nullable=True)
    menu_item = relationship("MenuItem", back_populates="order_details")
    order = relationship("Order", back_populates="order_details")
