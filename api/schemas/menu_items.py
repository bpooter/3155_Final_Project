from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class MenuCategory(str, Enum):
    SANDWICH = "sandwich"
    SIDE = "side"
    DRINK = "drink"
    DESSERT = "dessert"

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    calories: Optional[int] = None
    category: MenuCategory

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(MenuItemBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    calories: Optional[int] = None
    category: Optional[MenuCategory] = None

class MenuItem(MenuItemBase):
    menu_item_id: int

    class ConfigDict:
        from_attributes = True