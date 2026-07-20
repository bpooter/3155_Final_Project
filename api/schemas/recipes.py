from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class RecipeBase(BaseModel):
    menu_item_id: int
    resource_id: int
    quantity_required: Decimal

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    quantity_required: Optional[Decimal] = None

class Recipe(RecipeBase):
    recipe_id: int

    class ConfigDict:
        from_attributes = True