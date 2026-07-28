from decimal import Decimal

import pytest
from fastapi import HTTPException

from ..models.payments import PaymentType
from ..schemas.checkout import CheckoutRequest, CheckoutItem
from ..services.checkout_service import validate_customer, calculate_subtotal


def test_validate_customer_guest():
    request = CheckoutRequest(
        customer_id= None,
        guest_name = "John",
        guest_email= "test@validate.com",
        guest_phone="123-213-3322",
        payment_type=PaymentType.CARD,
        items=[]
    )

    validate_customer(request)

def test_validate_customer_both():
    request = CheckoutRequest(
        customer_id= 1,
        guest_name = "John",
        guest_email= "test@validate.com",
        guest_phone="123-213-3322",
        payment_type=PaymentType.CARD,
        items=[]
    )

    with pytest.raises(HTTPException):
        validate_customer(request)

def test_validate_customer_account():
    request = CheckoutRequest(
        customer_id= 1,
        guest_name = None,
        guest_email = None,
        guest_phone = None,
        payment_type=PaymentType.CARD,
        items=[]
    )

    validate_customer(request)

def test_validate_customer_none():
    request = CheckoutRequest(
        customer_id= None,
        guest_name = None,
        guest_email = None,
        guest_phone = None,
        payment_type=PaymentType.CARD,
        items=[]
    )

    with pytest.raises(HTTPException):
        validate_customer(request)

def test_calculate_subtotal(mocker):
    request = CheckoutRequest(
        payment_type=PaymentType.CARD,
        items=[
            CheckoutItem(
                menu_item_id=1,
                quantity=2
            )
        ]
    )

    mock_menu_item = mocker.Mock()
    mock_menu_item.price = Decimal("5.00")

    mocker.patch(
        "api.services.checkout_service.menu_items.read_one",
        return_value=mock_menu_item
    )

    result = calculate_subtotal(None, request)

    assert result == Decimal("10.00")