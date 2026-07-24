from decimal import Decimal
from pydantic import BaseModel


class RecipeBase(BaseModel):
    menu_item_id: int
    resource_id: int
    quantity_required: Decimal


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    quantity_required: Decimal | None = None


class Recipe(RecipeBase):
    recipe_id: int

    class ConfigDict:
        from_attributes = True