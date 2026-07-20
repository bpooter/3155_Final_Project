from enum import Enum

from sqlalchemy import Column, Integer, String, DECIMAL, Enum as SQLEnum
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Unit(str, Enum):
    EACH = "each"
    SLICE = "slice"
    OUNCE = "ounce"
    POUND = "pound"

class Resource(Base):
    __tablename__ = "resources"

    resource_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_name = Column(String(100), unique=True, nullable=False)
    quantity_on_hand = Column(DECIMAL(10,2), index=True, nullable=False, server_default='0.00')
    unit = Column(SQLEnum(Unit), nullable=False)
    recipes = relationship("Recipe", back_populates="resource")
