from decimal import Decimal

from fastapi import HTTPException, status

from . import inventory_service
from ..controllers import menu_items
from ..controllers import promotions
from ..controllers.orders import generate_tracking_number
from ..models import order_details as order_details_model
from ..models import orders as order_model
from ..models import payments as payment_model
from ..models.payments import TransactionStatus, PaymentType
from ..schemas.promotions import DiscountType


def validate_customer(request):

    has_account = request.customer_id is not None

    has_guest = request.guest_name is not None and request.guest_email is not None and request.guest_phone is not None

    if has_account and has_guest:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot provide both account and guest information")

    if not has_account and not has_guest:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Information for customer is required")



def validate_menu_items(db, request):
    for item in request.items:
        menu_items.read_one(db, item.menu_item_id)


def calculate_subtotal(db, request):
    subtotal = Decimal("0.00")

    for item in request.items:
        menu_item = menu_items.read_one(db, item.menu_item_id)
        subtotal += menu_item.price * item.quantity

    return subtotal


def apply_promotion(db, request, subtotal):

    if request.promotion_code is None:
        return {
            "discount_amount": Decimal("0.00"),
            "promotion_id": None
        }

    promotion = promotions.read_by_code(
        request.promotion_code,
        db
    )

    if not promotion.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Promotion code is not active!"
        )

    if promotion.discount_type == DiscountType.PERCENTAGE:
        discount = (
            subtotal *
            Decimal(str(promotion.discount_amount)) /
            Decimal("100")
        )

    elif promotion.discount_type == DiscountType.FIXED:
        discount = Decimal(str(promotion.discount_amount))

    elif promotion.discount_type == DiscountType.ITEM:
        discount = Decimal("0.00")

    return {
        "discount_amount": discount,
        "promotion_id": promotion.promotion_id
    }

def create_payment(db, order, request, total):

    if request.payment_type == PaymentType.CARD:
        if request.card_last_four is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Card last four is required for card payments")

    if request.payment_type == PaymentType.CASH:
        request.card_last_four = None

    new_payment = payment_model.Payment(
        order_id=order.order_id,
        payment_type=request.payment_type,
        amount=total,
        transaction_status=TransactionStatus.COMPLETED,
        card_last_four=request.card_last_four
    )

    db.add(new_payment)

    return new_payment

def create_order(db, request, subtotal, discount_amount, total, promotion_id):
        new_order = order_model.Order(
            tracking_number=generate_tracking_number(),
            customer_id=request.customer_id,
            guest_name=request.guest_name,
            guest_email=request.guest_email,
            guest_phone=request.guest_phone,
            order_type=request.order_type,
            subtotal=subtotal,
            discount_amount=discount_amount,
            total_price=total,
            promotion_id=promotion_id
        )

        db.add(new_order)
        db.flush()

        return new_order

def create_order_details(db, order, request):
    for item in request.items:
        menu_item = menu_items.read_one(db, item.menu_item_id)

        new_order_detail = order_details_model.OrderDetail(
            order_id = order.order_id,
            menu_item_id = item.menu_item_id,
            quantity = item.quantity,
            unit_price = menu_item.price,
            special_instructions = item.special_instructions
        )

        db.add(new_order_detail)

def place_order(db, request):

    try:

        validate_customer(request)

        validate_menu_items(db, request)

        subtotal = calculate_subtotal(db, request)

        promotion_result = apply_promotion(
            db,
            request,
            subtotal
        )

        discount_amount = promotion_result["discount_amount"]
        promotion_id = promotion_result["promotion_id"]

        total = subtotal - discount_amount

        inventory_service.check_inventory(db, request)

        order = create_order(
            db,
            request,
            subtotal,
            discount_amount,
            total,
            promotion_id
        )

        create_order_details(
            db,
            order,
            request
        )

        create_payment(
            db,
            order,
            request,
            total
        )

        inventory_service.deduct_inventory(db, request)

        db.commit()

        db.refresh(order)

        return order

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise

