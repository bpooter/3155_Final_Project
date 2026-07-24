from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from ..models import recipes as model
from ..models.menu_items import MenuItem
from ..models.resources import Resource
from ..schemas.recipes import RecipeCreate, RecipeUpdate


def create(request: RecipeCreate, db: Session):

    menu_item = (
        db.query(MenuItem)
        .filter(MenuItem.menu_item_id == request.menu_item_id)
        .first()
    )

    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )

    resource = (
        db.query(Resource)
        .filter(Resource.resource_id == request.resource_id)
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )

    new_recipe = model.Recipe(
        menu_item_id=request.menu_item_id,
        resource_id=request.resource_id,
        quantity_required=request.quantity_required
    )

    try:
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recipe already exists for this menu item and resource"
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return new_recipe

def read_all(db: Session):
    return db.query(model.Recipe).all()

def read_one(recipe_id: int, db: Session):

    recipe = (
        db.query(model.Recipe)
        .filter(model.Recipe.recipe_id == recipe_id)
        .first()
    )

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found"
        )

    return recipe

def update(
    recipe_id: int,
    request: RecipeUpdate,
    db: Session
):

    try:
        recipe = (
            db.query(model.Recipe)
            .filter(model.Recipe.recipe_id == recipe_id)
            .first()
        )

        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )

        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(recipe, key, value)

        db.commit()
        db.refresh(recipe)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return recipe

def delete(recipe_id: int, db: Session):

    try:
        recipe = (
            db.query(model.Recipe)
            .filter(model.Recipe.recipe_id == recipe_id)
            .first()
        )

        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )

        db.delete(recipe)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)