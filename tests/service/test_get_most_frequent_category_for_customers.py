from decimal import Decimal
from src.app.model import Customer
from src.app.service import PurchasesService


def test_get_most_frequent_category_for_customers(mock_purchases_service: PurchasesService):
    expected_result = {
        'Electronics': [Customer(id=1, first_name="John", last_name="Doe", age=30, cash=Decimal('1000.00'))],
        'Clothing': [Customer(id=2, first_name="Jane", last_name="Doe", age=25, cash=Decimal('1500.00'))]
    }
    assert mock_purchases_service.get_most_frequent_category_for_customers() == expected_result


def test_get_most_frequent_category_for_customers_with_empty_setup(mock_empty_purchases_service: PurchasesService):
    assert mock_empty_purchases_service.get_most_frequent_category_for_customers() == {}