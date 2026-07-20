from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from models.resources import Unit

'''
    resource_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_name = Column(String(100), unique=True, nullable=False)
    quantity_on_hand = Column(DECIMAL(10,2), index=True, nullable=False, server_default='0.00')
    unit = Column(SQLEnum(Unit), nullable=False)
'''


class ResourceBase(BaseModel):
    item_name: str
    quantity_on_hand: int
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
