from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response

from ..models import menu_items as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):

    new_item = model.MenuItem(
        item_name=request.item_name,
        description=request.description,
        price=request.price,
        calories=request.calories,
        category=request.category
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return new_item


def read_all(db: Session):

    try:
        result = db.query(model.MenuItem).all()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return result


def read_one(db: Session, menu_item_id):

    try:
        item = (
            db.query(model.MenuItem)
            .filter(
                model.MenuItem.menu_item_id == menu_item_id
            )
            .first()
        )

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found!"
            )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return item


def read_by_category(db: Session, category):

    try:
        items = (
            db.query(model.MenuItem)
            .filter(
                model.MenuItem.category == category
            )
            .all()
        )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return items


def update(db: Session, menu_item_id, request):

    try:
        item = (
            db.query(model.MenuItem)
            .filter(
                model.MenuItem.menu_item_id == menu_item_id
            )
            .first()
        )

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found!"
            )

        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(item, key, value)

        db.commit()
        db.refresh(item)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return item


def delete(db: Session, menu_item_id):

    try:
        item = (
            db.query(model.MenuItem)
            .filter(
                model.MenuItem.menu_item_id == menu_item_id
            )
            .first()
        )

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found!"
            )

        db.delete(item)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)