from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from ..models import resources as model
from ..schemas.resources import ResourceCreate, ResourceUpdate


def create(request: ResourceCreate, db: Session):

    new_resource = model.Resource(
        item_name=request.item_name,
        quantity_on_hand=request.quantity_on_hand,
        unit=request.unit,
    )

    try:
        db.add(new_resource)
        db.commit()
        db.refresh(new_resource)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Resource already exists"
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return new_resource

def read_all(db: Session):
    return db.query(model.Resource).all()

def read_one(resource_id: int, db: Session):

    resource = (
        db.query(model.Resource)
        .filter(model.Resource.resource_id == resource_id)
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {resource_id} not found"
        )

    return resource

def update(
    resource_id: int,
    request: ResourceUpdate,
    db: Session
):

    try:
        resource = (
            db.query(model.Resource)
            .filter(
                model.Resource.resource_id == resource_id
            )
            .first()
        )

        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )

        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(resource, key, value)

        db.commit()
        db.refresh(resource)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resource already exists"
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return resource

def delete(resource_id: int, db: Session):

    try:
        resource = (
            db.query(model.Resource)
            .filter(
                model.Resource.resource_id == resource_id
            )
            .first()
        )

        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )

        db.delete(resource)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
