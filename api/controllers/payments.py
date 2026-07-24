from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..schemas.payments import PaymentCreate, PaymentUpdate
from ..models import payments as model


def create(request: PaymentCreate, db: Session):

    new_payment = model.Payment(
        order_id=request.order_id,
        payment_type=request.payment_type,
        amount=request.amount,
        transaction_status=request.transaction_status,
        card_last_four=request.card_last_four
    )
    try:
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return new_payment

def read_all(db: Session):

    try:
        payments = db.query(model.Payment).all()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return payments

def read_one(payment_id: int, db: Session):

    try:
        payment = (db.query(model.Payment)
                   .filter(model.Payment.payment_id == payment_id)
                   .first()
                   )

        if payment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment with id {payment_id} not found"
            )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return payment

def update(payment_id: int, request: PaymentUpdate, db: Session):

    try:
        payment = (db.query(model.Payment)
                   .filter(model.Payment.payment_id==payment_id)
                   .first()
                   )
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment with id {payment_id} not found"
            )

        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(payment, key, value)

        db.commit()
        db.refresh(payment)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


    return payment

def delete(payment_id: int, db: Session):
    try:
        payment = (db.query(model.Payment)
                   .filter(model.Payment.payment_id == payment_id)
                   .first()
                   )
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment with id {payment_id} not found"
            )

        db.delete(payment)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)