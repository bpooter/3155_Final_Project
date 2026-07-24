from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..controllers import resources as controller
from ..schemas import resources as schema
from ..dependencies.database import get_db


router = APIRouter(
    tags=["Resources"],
    prefix="/resources"
)


@router.post("/", response_model=schema.Resource, status_code=status.HTTP_201_CREATED)
def create(
    request: schema.ResourceCreate,
    db: Session = Depends(get_db)
):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Resource])
def read_all(
    db: Session = Depends(get_db)
):
    return controller.read_all(db=db)


@router.get("/{resource_id}", response_model=schema.Resource)
def read_one(
    resource_id: int,
    db: Session = Depends(get_db)
):
    return controller.read_one(resource_id=resource_id, db=db)


@router.put("/{resource_id}", response_model=schema.Resource)
def update(
    resource_id: int,
    request: schema.ResourceUpdate,
    db: Session = Depends(get_db)
):
    return controller.update(
        db=db,
        request=request,
        resource_id=resource_id
    )


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    resource_id: int,
    db: Session = Depends(get_db)
):
    return controller.delete(
        db=db,
        resource_id=resource_id
    )