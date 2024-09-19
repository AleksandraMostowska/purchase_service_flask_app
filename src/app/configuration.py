import os
from src.app.data.repository import customer_product_repository_csv, customer_product_repository_json
from src.app.data.database.repository import customer_product_repository_sql
from src.app.service import PurchasesService
from dotenv import load_dotenv
load_dotenv()

repo_type = os.getenv("SOURCE")
"""
Create an instance of PurchasesService based on the repository type.

- If the repository type is "sql", use the SQL-based repository.
- If the repository type is "csv", use the CSV-based repository.
- If the repository type is "json", use the JSON-based repository.
- Raise a ValueError if the repository type is unsupported.

The PurchasesService is initialized with the appropriate repository, allowing the service
to interact with different data sources as specified by the environment configuration.
"""
match repo_type:
    case "sql":
        purchase_service = PurchasesService(customer_product_repository=customer_product_repository_sql)
    case "csv":
        purchase_service = PurchasesService(customer_product_repository=customer_product_repository_csv)
    case "json":
        purchase_service = PurchasesService(customer_product_repository=customer_product_repository_json)
    case _:
        raise ValueError("Unsupported repository type")
