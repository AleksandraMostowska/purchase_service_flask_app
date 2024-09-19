from decimal import Decimal
from src.app.model import Customer
from src.app.service import PurchasesService


def test_customer_spending_in_category(mock_purchases_service: PurchasesService):
    expected_customers = [
        Customer(id=1, first_name="John", last_name="Doe", age=30, cash=Decimal('1000.00'))
    ]
    result = mock_purchases_service.get_most_spending_in_category("Electronics")
    assert len(result) == len(expected_customers)
    assert all(c in result for c in expected_customers)


def test_no_spending_in_category(mock_purchases_service: PurchasesService):
    expected_customers = []
    result = mock_purchases_service.get_most_spending_in_category("Book")
    assert len(result) == len(expected_customers)
    assert all(c in result for c in expected_customers)


def test_empty_purchases(mock_empty_purchases_service: PurchasesService):
    expected_customers = []
    result = mock_empty_purchases_service.get_most_spending_in_category("Electronics")
    assert len(result) == len(expected_customers)
    assert all(c in result for c in expected_customers)
