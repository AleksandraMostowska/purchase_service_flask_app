import os
from decimal import Decimal
from io import StringIO
import requests
import csv
from src.app.model import Purchase, Customer, Product
from src.app.data.database.repository import CrudRepository
from dotenv import load_dotenv

load_dotenv()


class NotImplementedOperationsRepository[T](CrudRepository[T]):

    def find_by_id(self, entity_id: int) -> Purchase | None:
        """
        Raises an exception since finding by ID is not supported for CSV repositories.

        :param entity_id: The ID of the entity to find.
        :raises NotImplementedError: Indicates that this operation is not supported.
        """
        raise NotImplementedError("CSV repository does not support finding by id.")

    def save_or_update(self, entity: Purchase) -> None:
        """
        Raises an exception since saving or updating is not supported for CSV repositories.

        :param entity: The entity to save or update.
        :raises NotImplementedError: Indicates that this operation is not supported.
        """
        raise NotImplementedError("CSV repository does not support saving data.")

    def save_or_update_many(self, entities: list[Purchase]) -> None:
        """
        Raises an exception since saving or updating multiple entities is not supported for CSV repositories.

        :param entities: A list of entities to save or update.
        :raises NotImplementedError: Indicates that this operation is not supported.
        """
        raise NotImplementedError("CSV repository does not support saving data.")

    def delete_by_id(self, entity_id: int) -> None:
        """
        Raises an exception since deleting by ID is not supported for CSV repositories.

        :param entity_id: The ID of the entity to delete.
        :raises NotImplementedError: Indicates that this operation is not supported.
        """
        raise NotImplementedError("CSV repository does not support deleting data.")

    def delete_all(self) -> None:
        """
        Raises an exception since deleting all data is not supported for CSV repositories.

        :raises NotImplementedError: Indicates that this operation is not supported.
        """
        raise NotImplementedError("CSV repository does not support deleting data.")

    def find_all(self) -> list[T]:
        """
        This method is meant to retrieve and return all entities of type T from the repository.
        In this base class, it is not implemented and should be overridden by any subclass
        that uses this repository. The return type is a list of entities of type T.

        :return: A list of entities of type T.
        """
        pass

    def get_purchases(self) -> Purchase:
        """
        This method is intended to retrieve and return all purchase records from the repository.
        In this base class, it is not implemented and must be overridden by any subclass that
        handles customer purchases. The return type is a Purchase object containing details of
        the purchases.

        :return: A Purchase object containing the details of all purchases.
        """
        pass


class CustomerProductRepositoryCSV(NotImplementedOperationsRepository[Purchase]):
    """
    Repository class for handling customer and product data stored in a CSV file.

    This class implements CRUD operations for reading data from a CSV file.
    """

    def __init__(self, path: str) -> None:
        """
        Initializes the repository with the path to the CSV file.

        :param path: The file path to the CSV file containing customer and product data.
        """
        self.path = path

    def find_all(self) -> list[Purchase]:
        """
        Retrieves all purchases from the CSV file.

        :return: A list containing a single Purchase object with customer and product data.
        """
        response = requests.get(self.path)
        csv_content = response.text
        csv_file = StringIO(csv_content)
        reader = csv.DictReader(csv_file)

        customers = {}
        purchases = {}

        for row in reader:
            customer_id = int(row['ID']) if row['ID'] else None
            if customer_id is None:
                continue

            if customer_id not in customers:
                customers[customer_id] = Customer(
                    id=customer_id,
                    first_name=row['FirstName'] if row['FirstName'] else '',
                    last_name=row['LastName'] if row['LastName'] else '',
                    age=int(row['Age']) if row['Age'] else 0,
                    cash=Decimal(row['Salary']) if row['Salary'] else Decimal('0.00')
                )
                purchases[customers[customer_id]] = []

            if row['ProductID']:
                product = Product(
                    id=int(row['ProductID']),
                    name=row['Product'] if row['Product'] else '',
                    category=row['Category'] if row['Category'] else '',
                    price=Decimal(row['Price']) if row['Price'] else Decimal('0.00')
                )
                purchases[customers[customer_id]].append(product)

        return [Purchase(customers_and_their_products=purchases)]


    def get_purchases(self) -> Purchase:
        """
        Retrieves a single Purchase object representing all purchases.

        :return: A Purchase object with customer and product data.
        """
        return self.find_all()[0]


class CustomerProductRepositoryJSON(NotImplementedOperationsRepository[Purchase]):
    """
    Repository class for handling customer and product data stored in a JSON file.

    This class implements CRUD operations for reading data from a JSON file.
    """

    def __init__(self, path: str) -> None:
        """
        Initializes the repository with the URL to the JSON file.

        :param path: The URL to the JSON file containing customer and product data.
        """
        self.path = path

    def find_all(self) -> list[Purchase]:
        """
        Retrieves all purchases from the JSON file.

        :return: A list containing a single Purchase object with customer and product data.
        """
        response = requests.get(self.path)
        data = response.json()

        customers = {}
        purchases = {}

        for entry in data:

            customer_id = entry['ID']
            if customer_id not in customers:
                customers[customer_id] = Customer(
                    id=customer_id,
                    first_name=entry['FirstName'],
                    last_name=entry['LastName'],
                    age=entry['Age'],
                    cash=Decimal(entry['Salary'])
                )

            if customers[customer_id] not in purchases:
                purchases[customers[customer_id]] = []

            for purchase in entry.get('Purchases', []):
                product = Product(
                    id=purchase['ProductID'],
                    name=purchase['Product'],
                    category=purchase['Category'],
                    price=Decimal(purchase['Price'])
                )
                purchases[customers[customer_id]].append(product)

        return [Purchase(customers_and_their_products=purchases)]

    def get_purchases(self) -> Purchase:
        """
        Retrieves a single Purchase object representing all purchases.

        :return: A Purchase object with customer and product data.
        """
        return self.find_all()[0]


# ======================================================================================================================
customer_product_repository_csv = CustomerProductRepositoryCSV(path=os.getenv("CSV_PATH"))
customer_product_repository_json = CustomerProductRepositoryJSON(path=os.getenv("JSON_PATH"))
