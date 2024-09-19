import pytest
from decimal import Decimal

from src.app.service import PurchasesService


@pytest.mark.parametrize("customer_id, expected_spent", [
    (1, Decimal('2000.00')),
    (2, Decimal('100.00'))
])
def test_with_customers(mock_purchases_service: PurchasesService, customer_id: int, expected_spent: Decimal):
    assert mock_purchases_service.get_customers_total_spent(customer_id) == expected_spent


def test_with_empty_setup(mock_empty_purchases_service: PurchasesService):
    assert mock_empty_purchases_service.get_customers_total_spent(1) == Decimal('0.00')
