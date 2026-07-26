from typing import Optional

from pydantic import BaseModel, Field
from ..models.orders import OrderType
from ..models.payments import PaymentType

class CheckoutItem(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0)
    special_instructions: Optional[str] = None

class CheckoutRequest(BaseModel):
    customer_id: Optional[int] = None
    guest_name: Optional[str] = None
    guest_email: Optional[str] = None
    guest_phone: Optional[str] = None
    order_type: OrderType = OrderType.TAKEOUT
    promotion_code: Optional[str] = None
    payment_type: PaymentType
    card_last_four: Optional[str] = None
    items: list[CheckoutItem]