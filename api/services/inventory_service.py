from fastapi import HTTPException
from starlette import status

from ..controllers import recipes


def check_inventory(db, request):

    for item in request.items:
        recipe_list = recipes.read_by_menu_item_id(item.menu_item_id, db)

        for recipe in recipe_list:
            quantity_required = recipe.quantity_required * item.quantity

            if recipe.resource.quantity_on_hand < quantity_required:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Not enough {recipe.resource.item_name}")


def deduct_inventory(db, request):

    for item in request.items:

        recipe_list = recipes.read_by_menu_item_id(item.menu_item_id, db)

        for recipe in recipe_list:

            amount_used = (
                recipe.quantity_required *
                item.quantity
            )

            recipe.resource.quantity_on_hand -= amount_used

