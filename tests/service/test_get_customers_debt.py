import pytest
from decimal import Decimal
from src.app.model import Customer
from src.app.service import PurchasesService


@pytest.mark.parametrize(
    "customer_id, expected_result",
    [
        (1, Decimal(1000)),
        (2, Decimal(0))
    ]
)
def test_when_customers_with_purchases(mock_purchases_service: PurchasesService, customer_id: int, expected_result: Decimal):
    assert mock_purchases_service.get_customers_debt(customer_id) == expected_result


@pytest.mark.parametrize(
    "customer_id, expected_result",
    [
        (1, Decimal(-1)),
        (2, Decimal(-1))
    ]
)
def test_with_empty_setup(mock_empty_purchases_service: PurchasesService, customer_id: int, expected_result: Decimal):
    assert mock_empty_purchases_service.get_customers_debt(customer_id) == expected_result


def test_when_no_purchases(mock_purchases_service: PurchasesService):
    new_customer = Customer(id=3, first_name="Sam", last_name="Smith", age=28, cash=Decimal('100.00'))
    mock_purchases_service.get_all_purchases().customers_and_their_products[new_customer] = []
    assert mock_purchases_service.get_customers_debt(3) == Decimal(0)
