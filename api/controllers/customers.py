from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response

from ..models import customers as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):

    new_customer = model.Customer(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        phone=request.phone,
        address=request.address
    )

    try:
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return new_customer


def read_all(db: Session):

    try:
        customers = db.query(model.Customer).all()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return customers


def read_one(db: Session, customer_id):

    try:
        customer = (
            db.query(model.Customer)
            .filter(model.Customer.customer_id == customer_id)
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found!"
            )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return customer


def update(db: Session, customer_id, request):

    try:
        customer = (
            db.query(model.Customer)
            .filter(model.Customer.customer_id == customer_id)
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found!"
            )

        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(customer, key, value)

        db.commit()
        db.refresh(customer)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return customer


def delete(db: Session, customer_id):

    try:
        customer = (
            db.query(model.Customer)
            .filter(model.Customer.customer_id == customer_id)
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found!"
            )

        db.delete(customer)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)