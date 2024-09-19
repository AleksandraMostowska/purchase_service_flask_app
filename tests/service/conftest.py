import pytest
from unittest.mock import MagicMock
from decimal import Decimal
from src.app.model import Customer, Product, Purchase
from src.app.service import PurchasesService
from src.app.data.database.repository import CrudRepository


@pytest.fixture
def mock_purchases_service() -> PurchasesService:
    """
    Fixture for creating a mock PurchasesService with predefined purchase data.

    :return: A PurchasesService instance with a mocked CrudRepository.
    """
    service = PurchasesService(customer_product_repository=MagicMock(spec=CrudRepository))
    mock_purchase = Purchase(customers_and_their_products={
        Customer(id=1, first_name="John", last_name="Doe", age=30, cash=Decimal('1000.00')): [
            Product(id=1, name="Laptop", category="Electronics", price=Decimal('1200.00')),
            Product(id=2, name="Smartphone", category="Electronics", price=Decimal('800.00'))
        ],
        Customer(id=2, first_name="Jane", last_name="Doe", age=25, cash=Decimal('1500.00')): [
            Product(id=3, name="Shoes", category="Clothing", price=Decimal('100.00'))
        ]
    })
    service.customer_product_repository.get_purchases = MagicMock(return_value=mock_purchase)

    return service




@pytest.fixture
def mock_empty_purchases_service() -> PurchasesService:
    """
    Fixture for creating a mock PurchasesService with empty purchase data.

    :return: A PurchasesService instance with a mocked CrudRepository.
    """
    service = PurchasesService(customer_product_repository=MagicMock(spec=CrudRepository))
    mock_empty_purchase = Purchase(customers_and_their_products={})
    service.customer_product_repository.get_purchases = MagicMock(return_value=mock_empty_purchase)
    return service

