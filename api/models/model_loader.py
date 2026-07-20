from . import orders, order_details, recipes, sandwiches, resources, promotions, payments, menu_items, customers

from ..dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    #sandwiches.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)

    #TODO remember to add new models to this so they are loaded
    promotions.Base.metadata.create_all(engine)
    payments.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    customers.Base.metadata.create_all(engine)
    