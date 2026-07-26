from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from ..models import promotions as model
from ..schemas.promotions import PromotionCreate, PromotionUpdate


def create(request: PromotionCreate, db: Session):

    new_promotion = model.Promotion(
        promotion_code=request.promotion_code,
        discount_type=request.discount_type,
        discount_amount=request.discount_amount,
        discount_item=request.discount_item,
        expiration_date=request.expiration_date
    )

    try:
        db.add(new_promotion)
        db.commit()
        db.refresh(new_promotion)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Promotion code already exists"
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return new_promotion

def read_all(db: Session):
    return db.query(model.Promotion).all()

def read_by_code(promotion_code: str, db: Session):
    return (
        db.query(model.Promotion)
        .filter(
            model.Promotion.promotion_code == promotion_code
        )
        .first()
    )

def read_one(promotion_id: int, db: Session):

    promotion = (
        db.query(model.Promotion)
        .filter(model.Promotion.promotion_id == promotion_id)
        .first()
    )

    if not promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Promotion with id {promotion_id} not found"
        )

    return promotion

def update(
    promotion_id: int,
    request: PromotionUpdate,
    db: Session
):

    try:
        promotion = (
            db.query(model.Promotion)
            .filter(
                model.Promotion.promotion_id == promotion_id
            )
            .first()
        )

        if not promotion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Promotion not found"
            )

        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(promotion, key, value)

        db.commit()
        db.refresh(promotion)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return promotion

def delete(promotion_id: int, db: Session):

    try:
        promotion = (
            db.query(model.Promotion)
            .filter(
                model.Promotion.promotion_id == promotion_id
            )
            .first()
        )

        if not promotion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Promotion not found"
            )

        db.delete(promotion)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
