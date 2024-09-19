from decimal import Decimal
from src.app.model import Product
from src.app.service import PurchasesService
from src.app.utils import MaxMin


def test_get_most_and_least_expensive_in_category(mock_purchases_service: PurchasesService):
    expected_result = {
        "Electronics": MaxMin(
            max=Product(id=1, name="Laptop", category="Electronics", price=Decimal('1200.00')),
            min=Product(id=2, name="Smartphone", category="Electronics", price=Decimal('800.00'))
        ),
        "Clothing": MaxMin(
            max=Product(id=3, name="Shoes", category="Clothing", price=Decimal('100.00')),
            min=Product(id=3, name="Shoes", category="Clothing", price=Decimal('100.00'))
        )
    }
    assert mock_purchases_service.get_most_and_least_expensive_in_category() == expected_result


def test_get_most_and_least_expensive_in_category_with_empty_setup(mock_empty_purchases_service: PurchasesService):
    assert mock_empty_purchases_service.get_most_and_least_expensive_in_category() == {}
