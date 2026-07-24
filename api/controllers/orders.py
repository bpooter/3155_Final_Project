import random
import string
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response

from ..models.promotions import Promotion
from ..models import orders as model
from sqlalchemy.exc import SQLAlchemyError

def generate_tracking_number():
    return "ITIS-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create(db: Session, request):

    print(f"Promotion code from request: '{request.promotion_code}'")

    try:
        promotion = None

        if request.promotion_code:
            promotion = (
                db.query(Promotion)
                .filter(Promotion.promotion_code == request.promotion_code)
                .first()
            )

            if not promotion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Promotion code not found!"
                )

        new_order = model.Order(
            tracking_number=generate_tracking_number(),
            customer_id=request.customer_id,
            guest_name=request.guest_name,
            order_type=request.order_type,
            guest_email=request.guest_email,
            guest_phone=request.guest_phone,
            promotion_id=promotion.promotion_id if promotion else None
        )

        db.add(new_order)
        db.commit()
        db.refresh(new_order)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return new_order


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return result


def read_one(db: Session, order_id):
    try:
        order = (
            db.query(model.Order)
            .filter(model.Order.order_id == order_id)
            .first()
        )

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Id not found!"
            )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return order


def update(db: Session, order_id, request):
    try:
        order = (
            db.query(model.Order)
            .filter(model.Order.order_id == order_id)
            .first()
        )

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Id not found!"
            )

        update_data = request.model_dump(exclude_unset=True)

        # Convert promotion_code into promotion_id
        if "promotion_code" in update_data:
            promotion_code = update_data.pop("promotion_code")

            promotion = (
                db.query(Promotion)
                .filter(Promotion.promotion_code == promotion_code)
                .first()
            )

            if not promotion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Promotion code not found!"
                )

            update_data["promotion_id"] = promotion.promotion_id

        for key, value in update_data.items():
            setattr(order, key, value)

        db.commit()
        db.refresh(order)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return order


def delete(db: Session, order_id):
    try:
        order = (
            db.query(model.Order)
            .filter(model.Order.order_id == order_id)
            .first()
        )

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Id not found!"
            )

        db.delete(order)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
