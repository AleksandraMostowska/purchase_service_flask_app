from decimal import Decimal
from src.app.model import Customer
from src.app.service import PurchasesService


def test_get_customers_with_debts(mock_purchases_service: PurchasesService):
    result = mock_purchases_service.get_customers_with_debts()
    expected_result = {
        1: Decimal('1000.00')
    }
    assert len(result) == len(expected_result)
    for customer, debt in expected_result.items():
        assert customer in result
        assert result[customer] == debt


def test_get_customers_with_debts_empty(mock_empty_purchases_service: PurchasesService):
    assert mock_empty_purchases_service.get_customers_with_debts() == {}


def test_when_no_purchases(mock_purchases_service: PurchasesService):
    new_customer = Customer(id=3, first_name="Sam", last_name="Smith", age=28, cash=Decimal('100.00'))
    mock_purchases_service.get_all_purchases().customers_and_their_products[new_customer] = []
    assert mock_purchases_service.get_customers_debt(3) == Decimal(0)