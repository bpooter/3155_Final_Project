from enum import Enum

from sqlalchemy import Column, Integer, ForeignKey, Enum as SQLEnum, DECIMAL, String
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class PaymentType(str, Enum):
    CASH = "cash"
    CARD = "card"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False, unique=True)
    payment_type = Column(SQLEnum(PaymentType), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    card_last_four = Column(String(4), nullable=True)
    transaction_status = Column(SQLEnum(TransactionStatus), nullable=False)
    order = relationship("Order", back_populates="payment")