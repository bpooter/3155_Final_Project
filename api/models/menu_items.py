from enum import Enum

from sqlalchemy import Column, Integer, String, DECIMAL, Enum as SQLEnum
from sqlalchemy.orm import relationship

from ..dependencies.database import Base

class MenuCategory(str, Enum):
    SANDWICH = "sandwich"
    SIDE = "side"
    DRINK = "drink"
    DESSERT = "dessert"

class MenuItem(Base):
    __tablename__ = "menu_items"

    menu_item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(DECIMAL(10,2), nullable=False)
    calories = Column(Integer, nullable=True)
    category = Column(SQLEnum(MenuCategory), nullable=False)
    order_details = relationship("OrderDetail", back_populates="menu_item")
    recipes = relationship("Recipe", back_populates="menu_item")