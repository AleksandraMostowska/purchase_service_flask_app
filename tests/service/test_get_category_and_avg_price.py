from decimal import Decimal

from src.app.service import PurchasesService


def test_get_category_and_avg_price(mock_purchases_service: PurchasesService):
    expected = {
        "Electronics": Decimal('1000.00'),
        "Clothing": Decimal('100.00')
    }
    assert mock_purchases_service.get_category_and_avg_price() == expected


def test_with_empty_setup(mock_empty_purchases_service: PurchasesService):
    assert mock_empty_purchases_service.get_category_and_avg_price() == {}
