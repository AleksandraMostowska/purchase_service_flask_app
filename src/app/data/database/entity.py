from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column
)
from sqlalchemy import (
    Integer,
    String,
    Numeric,
    ForeignKey
)
from decimal import Decimal
from src.app.data.database.configuration import sa


class CustomerProductEntity(sa.Model):
    """
    SQLAlchemy model representing the association between customers and products.

    This model is used to create a many-to-many relationship between customers and products
    through a join table 'customer_product'.
    """
    __tablename__ = 'customer_product'

    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.id'), primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), primary_key=True)

    def __str__(self):
        """
        String representation of the CustomerProductEntity.

        :return: A string representation of the entity, showing customer and product IDs.
        """
        return f'CUSTOMER_PRODUCT: customer_id={self.customer_id}, product_id={self.product_id}'

    def __repr__(self):
        """
        Official string representation of the CustomerProductEntity.

        :return: A string representation of the entity, using __str__ method.
        """
        return str(self)


class CustomerEntity(sa.Model):
    """
    SQLAlchemy model representing a customer.

    This model represents a customer in the system with attributes such as ID, first name,
    last name, age, and cash balance. It also defines a many-to-many relationship with products.
    """
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(length=255))
    last_name: Mapped[str] = mapped_column(String(length=255))
    age: Mapped[int] = mapped_column(Integer)
    cash: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    purchases = relationship('ProductEntity', secondary='customer_product', back_populates='buyers')

    def __str__(self):
        """
        String representation of the CustomerEntity.

        :return: A string representation of the customer, including first name, last name, age, and cash balance.
        """
        return f'CUSTOMER: {self.first_name} {self.last_name} {self.age} {self.cash}'

    def __repr__(self):
        """
        Official string representation of the CustomerEntity.

        :return: A string representation of the entity, using __str__ method.
        """
        return str(self)


class ProductEntity(sa.Model):
    """
    SQLAlchemy model representing a product.

    This model represents a product in the system with attributes such as ID, name,
    category, and price. It also defines a many-to-many relationship with customers.
    """
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=255))
    category: Mapped[str] = mapped_column(String(length=255))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    buyers = relationship('CustomerEntity', secondary='customer_product', back_populates='purchases')

    def __str__(self):
        """
        String representation of the ProductEntity.

        :return: A string representation of the product, including name, category, and price.
        """
        return f'PRODUCT: {self.name} {self.category} {self.price}'

    def __repr__(self):
        """
        Official string representation of the ProductEntity.

        :return: A string representation of the entity, using __str__ method.
        """
        return str(self)
