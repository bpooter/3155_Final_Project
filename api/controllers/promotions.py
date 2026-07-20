from datetime import date

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import promotions as model
from ..models.order_details import OrderDetail
from sqlalchemy.exc import SQLAlchemyError

def get_all_promotions(db: Session):
    return db.query(model.Promotion).all()

def get_all_active_promotions(db: Session):
    return (
        db.query(model.Promotion)
        .filter(model.Promotion.active.is_(True))
        .all()
    )

def get_all_item_promotions(db: Session):
    return (
        db.query(model.Promotion)
        .filter(model.Promotion.discount_type == "item")
        .all
    )

def update_promotion(db: Session, promotion: model.Promotion, promotion_code: str):
    #TODO fix this function
    pass

def delete_promotion(db: Session, promotion_code: str):
    #TODO finish this function
    pass

def find_promotion_by_code(db: Session, promotion_code: str):
    return (db.query(model.Promotion)
            .filter(model.Promotion.promotion_code == promotion_code)
            .first()
            )

def apply_promotion(db: Session, order_id: int, promotion_code: str):
    promotion = find_promotion_by_code(db, promotion_code)

    if not promotion.active:
        raise HTTPException(status_code=404, detail="Promotion is inactive")

    if promotion.expiration_date < date.today():
        raise HTTPException(status_code=404, detail="Promotion has expired")

    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion does not exist")
    #TODO finish this to apply the discount

    order_details = (db.query(model.OrderDetail)
                     .filter(OrderDetail.order_id == order_id)
                     .all()
                     )

    subtotal = sum(
        detail.amount #TODO fix this to be total for this from the models/order_details.py
        for detail in order_details
    )
    if promotion.discount_type == "percentage":
        discount = subtotal * (promotion.discount_amount / 100)

    elif promotion.discount_type == "fixed":
        discount = promotion.discount_amount

    elif promotion.discount_type == "item":
        discount = 0
        #TODO handle the item logic

    return discount
