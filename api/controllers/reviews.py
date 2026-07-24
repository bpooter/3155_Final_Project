from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from ..models import reviews as model
from ..schemas.reviews import ReviewCreate, ReviewUpdate


def create(request: ReviewCreate, db: Session):

    new_review = model.Review(
        customer_id=request.customer_id,
        order_id=request.order_id,
        rating=request.rating,
        comment=request.comment
    )

    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Review already exists for that order"
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return new_review

def read_all(db: Session):
    return db.query(model.Review).all()

def read_one(review_id: int, db: Session):

    review = (
        db.query(model.Review)
        .filter(model.Review.review_id == review_id)
        .first()
    )

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found"
        )

    return review

def update(
    review_id: int,
    request: ReviewUpdate,
    db: Session
):

    try:
        review = (
            db.query(model.Review)
            .filter(
                model.Review.review_id == review_id
            )
            .first()
        )

        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )

        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(review, key, value)

        db.commit()
        db.refresh(review)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return review

def delete(review_id: int, db: Session):

    try:
        review = (
            db.query(model.Review)
            .filter(
                model.Review.review_id == review_id
            )
            .first()
        )

        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )

        db.delete(review)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
