from abc import ABC, abstractmethod
from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy
from src.app.data.database.configuration import sa
from src.app.data.database.entity import (
    ProductEntity,
    CustomerEntity,
    CustomerProductEntity
)
import logging

from src.app.model import Customer, Product, Purchase

logging.basicConfig(level=logging.INFO)


class CrudRepository[T](ABC):
    """
    An abstract base class for defining a generic CRUD (Create, Read, Update, Delete) repository.
    This class defines the contract that any repository (e.g., SQL, CSV, JSON) must follow to handle
    basic database operations for a specific entity type.
    """

    @abstractmethod
    def save_or_update(self, entity: T) -> None:
        """
        Saves or updates the given entity in the data store.

        :param entity: The entity to be saved or updated.
        """
        pass

    @abstractmethod
    def save_or_update_many(self, entities: list[T]) -> None:
        """
        Saves or updates multiple entities in the data store.

        :param entities: A list of entities to be saved or updated.
        """
        pass

    @abstractmethod
    def find_by_id(self, entity_id: int) -> T | None:
        """
        Finds an entity by its ID in the data store.

        :param entity_id: The ID of the entity to be found.
        :return: The entity if found, otherwise None.
        """
        pass

    @abstractmethod
    def find_all(self) -> list[T]:
        """
        Retrieves all entities from the data store.

        :return: A list of all entities.
        """
        pass

    @abstractmethod
    def delete_by_id(self, entity_id: int) -> None:
        """
        Deletes an entity from the data store by its ID.

        :param entity_id: The ID of the entity to be deleted.
        """
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """
        Deletes all entities of this type from the data store.
        """
        pass

    @abstractmethod
    def get_purchases(self) -> Purchase:
        """
        Retrieves all customer purchases from the data store.

        :return: A Purchase object containing details of all purchases made by customers.
        """
        pass


class CrudRepositoryORM[T: sa.Model](CrudRepository[T]):
    """
    A generic repository class for handling CRUD operations using SQLAlchemy ORM.
    This class provides implementations for saving, updating, finding, and deleting
    entities in a relational database using SQLAlchemy.
    """

    def __init__(self, db: SQLAlchemy) -> None:
        """
        Initializes the repository with a SQLAlchemy database connection.

        :param db: The SQLAlchemy instance to be used for database operations.
        """
        self.sa = db
        # Determines the entity type by inspecting the generic type parameter (T).
        self.entity_type = self.__class__.__orig_bases__[0].__args__[0]

    def save_or_update(self, entity: T) -> None:
        """
        Saves or updates the given entity in the database.

        :param entity: The entity to be saved or updated.
        """
        self.sa.session.add(entity)
        self.sa.session.commit()

    def save_or_update_many(self, entities: list[T]) -> None:
        """
        Saves or updates multiple entities in the database.

        :param entities: A list of entities to be saved or updated.
        """
        self.sa.session.add_all(entities)
        self.sa.session.commit()

    def find_by_id(self, entity_id: int) -> T | None:
        """
        Finds an entity by its ID.

        :param entity_id: The ID of the entity to be found.
        :return: The entity if found, otherwise None.
        """
        return self.sa.session.query(self.entity_type).get(entity_id)

    def find_all(self) -> list[T]:
        """
        Retrieves all entities from the database.

        :return: A list of all entities.
        """
        return sa.session.query(self.entity_type).all()

    def delete_by_id(self, entity_id: int) -> None:
        """
        Deletes an entity by its ID.

        :param entity_id: The ID of the entity to be deleted.
        """
        entity = self.find_by_id(entity_id)
        if entity:
            self.sa.session.delete(entity)
            self.sa.session.commit()

    def delete_all(self) -> None:
        """
        Deletes all entities from the database for this type.

        :return: None
        """
        self.sa.session.query(self.entity_type).delete()
        self.sa.session.commit()

    def get_purchases(self) -> Purchase:
        """
        This method is expected to be implemented in subclasses to retrieve purchases.
        It is a placeholder in this class and does not have a specific implementation.

        :return: A Purchase object containing details of purchases (to be implemented in subclass).
        """
        pass


class ProductRepositorySQL(CrudRepositoryORM[ProductEntity]):
    """
    A repository for handling product-related operations using SQLAlchemy ORM.
    """

    def __init__(self, db: SQLAlchemy):
        """
        Initializes the product repository with the provided SQLAlchemy database instance.

        :param db: The SQLAlchemy database instance.
        """
        super().__init__(db)

    def get_products(self) -> dict[int, Product]:
        """
        Retrieves all products from the database and returns them as a dictionary.

        :return: A dictionary where the keys are product IDs and the values are Product objects.
        """
        products = self.find_all()
        return {
            product.id: Product(
                id=product.id,
                name=product.name,
                category=product.category,
                price=product.price
            )
            for product in products
        }


class CustomerRepositorySQL(CrudRepositoryORM[CustomerEntity]):
    """
    A repository for handling customer-related operations using SQLAlchemy ORM.
    """

    def __init__(self, db: SQLAlchemy):
        """
        Initializes the customer repository with the provided SQLAlchemy database instance.

        :param db: The SQLAlchemy database instance.
        """
        super().__init__(db)

    def get_customers(self) -> dict[int, Customer]:
        """
        Retrieves all customers from the database and returns them as a dictionary.

        :return: A dictionary where the keys are customer IDs and the values are Customer objects.
        """
        customers = self.find_all()
        return {
            customer.id: Customer(
                id=customer.id,
                first_name=customer.first_name,
                last_name=customer.last_name,
                age=customer.age,
                cash=customer.cash
            )
            for customer in customers
        }


class CustomerProductRepositorySQL(CrudRepositoryORM[CustomerProductEntity]):
    """
    A repository for handling the relationship between customers and products using SQLAlchemy ORM.
    """

    def __init__(self, db: SQLAlchemy, product_repository: ProductRepositorySQL, customer_repository: CustomerRepositorySQL):
        """
        Initializes the customer-product repository with the provided SQLAlchemy database instance,
        product repository, and customer repository.

        :param db: The SQLAlchemy database instance.
        :param product_repository: A repository for fetching product information.
        :param customer_repository: A repository for fetching customer information.
        """
        super().__init__(db)
        self.product_repository = product_repository
        self.customer_repository = customer_repository

    def get_purchases(self) -> Purchase:
        """
        Retrieves all purchases by customers, mapping each customer to the products they purchased.

        :return: A Purchase object containing customers and their associated products.
        """
        customers = self.customer_repository.get_customers()
        products = self.product_repository.get_products()

        all_purchases = self.find_all()
        purchases = defaultdict(list)
        for cp in all_purchases:
            customer = customers.get(cp.customer_id)
            product = products.get(cp.product_id)
            if customer and product:
                purchases[customer].append(product)

        return Purchase(dict(purchases))


# ======================================================================================================================
customer_product_repository_sql = CustomerProductRepositorySQL(sa, product_repository=ProductRepositorySQL(sa),
                                                               customer_repository=CustomerRepositorySQL(sa))

