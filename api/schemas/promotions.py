from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from enum import Enum

class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"
    ITEM = "item"

class PromotionBase(BaseModel):
    promotion_code: str
    discount_type: DiscountType
    discount_amount: Decimal
    discount_item: Optional[str] = None
    expiration_date: date

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    promotion_code: Optional[str] = None #Potentially optional when updating
    discount_type: Optional[DiscountType] = None
    discount_amount: Optional[float] = None
    expiration_date: Optional[date] = None
    active: Optional[bool] = None

class Promotion(PromotionBase):
    promotion_id: int
    active: bool

    class ConfigDict:
        from_attributes = True

