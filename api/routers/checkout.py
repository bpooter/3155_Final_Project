from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..services import checkout_service
from ..schemas.checkout import CheckoutRequest

router = APIRouter(
    prefix="/checkout",
    tags=["Checkout"]
)


@router.post("/")
def checkout(
        request: CheckoutRequest,
        db: Session = Depends(get_db)
):

    return checkout_service.place_order(db,request)