from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, eq=True)
class Customer:
    """
    Represents a customer with their personal details and cash balance.
    """
    id: int
    first_name: str
    last_name: str
    age: int
    cash: Decimal

    def to_dict(self):
        """
        Converts the Customer instance to a dictionary format.

        :return: A dictionary with customer details.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "cash": str(self.cash)
        }


@dataclass(frozen=True, eq=True)
class Product:
    """
    Represents a product with its details.
    """
    id: int
    name: str
    category: str
    price: Decimal

    def to_dict(self):
        """
        Converts the Product instance to a dictionary format.

        :return: A dictionary with product details.
        """
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": str(self.price)
        }


@dataclass
class Purchase:
    """
    Represents the purchase information, including customers and the products they bought.
    """
    customers_and_their_products: dict[Customer, list[Product]]

    def to_dict(self):
        """
        Converts the Purchase instance to a dictionary format.

        :return: A dictionary mapping customer IDs to lists of product details.
        """
        return {
            str(customer.id): [product.to_dict() for product in products]
            for customer, products in self.customers_and_their_products.items()
        }

