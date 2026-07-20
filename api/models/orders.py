from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Float, Enum, func
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=True) #TODO reference the customer table and update the customer schema
    guest_name = Column(String(100), nullable=True)
    guest_email = Column(String(100), nullable=True)
    guest_phone = Column(String(20), nullable=True)
    order_date = Column(DATETIME, nullable=False, server_default=func.now())
    order_status = Column(
        Enum(
            "Pending",
            "Preparing",
            "Completed",
            "Cancelled"
        ),
        nullable=False,
        default="Pending"
    )

    subtotal = Column(DECIMAL(10,2), nullable=False)
    discount_amount = Column(DECIMAL(10,2), nullable=False, default=0.00)
    total_price = Column(DECIMAL(10,2), nullable=False)
    promotion_id = Column(Integer, ForeignKey('promotions.promotion_id'), nullable=True)
    order_details = relationship("OrderDetail", back_populates="order")
    promotion = relationship("Promotion", back_populates="orders")
    customer = relationship("Customer", back_populates="orders")
    payment = relationship("Payment", back_populates="order", uselist=False)