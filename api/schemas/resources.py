from decimal import Decimal
from pydantic import BaseModel
from typing import Optional

from ..models.resources import Unit


class ResourceBase(BaseModel):
    item_name: str
    quantity_on_hand: Decimal
    unit: Unit


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    item_name: Optional[str] = None
    quantity_on_hand: Optional[Decimal] = None
    unit: Optional[Unit] = None


class Resource(ResourceBase):
    resource_id: int

    class ConfigDict:
        from_attributes = True
