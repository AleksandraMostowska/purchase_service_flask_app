import pytest
from decimal import Decimal
from src.app.service import PurchasesService
from src.app.model import Customer


@pytest.mark.parametrize(
    "customer_id, expected_result",
    [
        (1, False),
        (2, True)
    ]
)
def test_with_sufficient_funds(mock_purchases_service: PurchasesService, customer_id: int, expected_result: bool):
    assert mock_purchases_service.can_customer_pay(customer_id) == expected_result


@pytest.mark.parametrize(
    "customer_id, expected_result",
    [
        (1, False),
        (2, False)
    ]
)
def test_with_empty_setup(mock_empty_purchases_service: PurchasesService, customer_id: int, expected_result: bool):
    assert mock_empty_purchases_service.can_customer_pay(customer_id) == expected_result


def test_when_no_purchases(mock_purchases_service: PurchasesService):
    new_customer = Customer(id=3, first_name="Sam", last_name="Smith", age=28, cash=Decimal('100.00'))
    mock_purchases_service.get_all_purchases().customers_and_their_products[new_customer] = []
    assert mock_purchases_service.can_customer_pay(3)

