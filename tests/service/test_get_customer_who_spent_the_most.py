from src.app.model import Customer
from decimal import Decimal

from src.app.service import PurchasesService


def test_with_customers(mock_purchases_service: PurchasesService):
    expected_customers = [
        Customer(id=1, first_name="John", last_name="Doe", age=30, cash=Decimal('1000.00'))
    ]
    result = mock_purchases_service.get_customer_who_spent_the_most()
    assert len(result) == len(expected_customers)
    assert all(c in result for c in expected_customers)


def test_with_empty_setup(mock_empty_purchases_service: PurchasesService):
    expected_customers = []
    result = mock_empty_purchases_service.get_customer_who_spent_the_most()
    assert len(result) == len(expected_customers)
    assert all(c in result for c in expected_customers)
