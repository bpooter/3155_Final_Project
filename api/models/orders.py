from enum import Enum

from sqlalchemy import (
    Column,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    DECIMAL,
    DATETIME,
    func
)
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class OrderType(str, Enum):
    TAKEOUT = "takeout"
    DELIVERY = "delivery"


class OrderStatus(str, Enum):
    PENDING = "Pending"
    PREPARING = "Preparing"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    tracking_number = Column(
        String(20),
        unique=True,
        nullable=False
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=True
    )

    guest_name = Column(String(100), nullable=True)
    guest_email = Column(String(100), nullable=True)
    guest_phone = Column(String(20), nullable=True)

    order_date = Column(
        DATETIME,
        nullable=False,
        server_default=func.now()
    )

    order_type = Column(
        SQLEnum(OrderType),
        nullable=False,
        default=OrderType.TAKEOUT
    )

    order_status = Column(
        SQLEnum(OrderStatus),
        nullable=False,
        default=OrderStatus.PENDING
    )

    subtotal = Column(
        DECIMAL(10, 2),
        nullable=False,
        default=0.00
    )

    discount_amount = Column(
        DECIMAL(10, 2),
        nullable=False,
        default=0.00
    )

    total_price = Column(
        DECIMAL(10, 2),
        nullable=False,
        default=0.00
    )

    promotion_id = Column(
        Integer,
        ForeignKey("promotions.promotion_id"),
        nullable=True
    )

    order_details = relationship(
        "OrderDetail",
        back_populates="order"
    )

    promotion = relationship(
        "Promotion",
        back_populates="orders"
    )

    customer = relationship(
        "Customer",
        back_populates="orders"
    )

    payment = relationship(
        "Payment",
        back_populates="order",
        uselist=False
    )

    review = relationship(
        "Review",
        back_populates="order",
        uselist=False
    )