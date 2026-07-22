from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, autoincrement=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False,
        unique=True
    )

    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    customer = relationship("Customer", back_populates="reviews")
    order = relationship("Order", back_populates="review")