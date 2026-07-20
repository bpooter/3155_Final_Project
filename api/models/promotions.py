from sqlalchemy import Column, Integer, String, Date, Float, Boolean, Enum, DECIMAL
from sqlalchemy.orm import relationship

from api.dependencies.database import Base



class Promotion(Base):
    __tablename__ = 'promotions'

    promotion_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promotion_code = Column(String(50), unique=True, nullable=False)
    discount_type = Column(Enum("percentage", "fixed", "item"), nullable=False)
    discount_amount = Column(DECIMAL(10,2), nullable=False)
    discount_item = Column(String(50), nullable=True)
    expiration_date = Column(Date, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    orders = relationship("Order", back_populates="promotion")