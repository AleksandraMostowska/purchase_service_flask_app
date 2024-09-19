import logging
from dataclasses import dataclass
from src.app.model import Purchase, Customer, Product
from decimal import Decimal
from collections import defaultdict
from src.app.utils import MaxMin
from src.app.data.database.repository import CrudRepository
logging.basicConfig(level=logging.INFO)


@dataclass
class PurchasesService:
    customer_product_repository: CrudRepository

    def get_all_purchases(self) -> Purchase:
        """
        Retrieves all purchases made by customers.

        :return: A Purchase object containing details of all customers and the products they purchased.
        """
        return self.customer_product_repository.get_purchases()

    def get_customers_total_spent(self, customer_id: int) -> Decimal:
        """
        Calculates the total amount spent by a customer with a given ID.

        :param customer_id: The ID of the customer whose spending is to be calculated.
        :return: The total amount spent by the customer. Returns 0 if the customer ID is not found.
        """
        customer_id_with_products = {c.id: p for c, p in self.get_all_purchases().customers_and_their_products.items()}
        return sum((Decimal(p.price) for p in customer_id_with_products.get(customer_id, [])), Decimal(0))

    def get_customer_who_spent_the_most(self) -> list[Customer]:
        """
        Identifies the customer(s) who have spent the most across all categories.

        :return: A list of customers who have spent the maximum amount. Returns an empty list if no customers are found.
        """
        customers_with_spent = {c: self.get_customers_total_spent(c.id)
                                for c, p in self.get_all_purchases().customers_and_their_products.items()}
        max_spent = max(customers_with_spent.values(), default=Decimal(0))
        return [c for c, spent in customers_with_spent.items() if spent.compare(max_spent) == 0]

    def get_most_spending_in_category(self, category: str) -> list[Customer]:
        """
        Finds the customer(s) who have spent the most in a specific category.

        :param category: The category for which to determine the highest spending customer(s).
        :return: A list of customers who have spent the most in the given category. Returns an empty list if no spending
        is recorded in the category.
        """
        customer_and_category_spent = {
            customer: sum(p.price for p in products if p.category == category)
            for customer, products in self.get_all_purchases().customers_and_their_products.items()
        }
        max_spent = max(customer_and_category_spent.values(), default=Decimal(0))
        return [] if max_spent == 0 \
            else [customer for customer, spent in customer_and_category_spent.items() if spent == max_spent]

    def get_age_category_preference(self) -> dict[int, str]:
        """
        Provides a summary of age groups and their most frequently purchased product categories.

        :return: A dictionary mapping each customer age to the product category they purchased most frequently.
        If no category is purchased for a specific age, the value will be None.
        """
        age_and_category_counts = defaultdict(lambda: defaultdict(int))

        for customer, products in self.get_all_purchases().customers_and_their_products.items():
            for product in products:
                age_and_category_counts[customer.age][product.category] += 1

        return {
            age: max(category_count.items(), key=lambda x: x[1], default=(None, 0))[0]
            for age, category_count in age_and_category_counts.items()
        }

    def get_category_and_avg_price(self) -> dict[str, Decimal]:
        """
        Calculates the average price of products in each category.

        :return: A dictionary where the key is the product category and the value is the average price of products
        in that category. Returns 0.00 if a category has no products.
        """
        category_with_prices = defaultdict(list)
        for product in self._get_unique_products().values():
            category_with_prices[product.category].append(product.price)

        return {
            cat: sum(prices) / Decimal(len(prices)) if prices else Decimal(0.00)
            for cat, prices in category_with_prices.items()
        }

    def get_most_and_least_expensive_in_category(self) -> dict[str, MaxMin]:
        """
        Identifies the most and least expensive products in each category.

        :return: A dictionary where the key is the product category and the value is an instance of `MaxMin`
        containing the most and least expensive products in that category. Returns None for both values
        if a category has no products.
        """
        category_with_products = defaultdict(list)
        for product in self._get_unique_products().values():
            category_with_products[product.category].append(product)

        return {
            category: MaxMin(
                max=max(products, key=lambda p: p.price, default=None),
                min=min(products, key=lambda p: p.price, default=None)
            )
            for category, products in category_with_products.items()
        }

    def get_most_frequent_category_for_customers(self) -> dict[str, list[Customer]]:
        """
        Determines the most frequently purchased product category for each customer.

        :return: A dictionary where the key is the product category and the value is a list of customers
        who have purchased that category the most frequently.
        Returns an empty list if no customers have purchased a category.
        """
        category_customer_count = defaultdict(lambda: defaultdict(int))
        for customer, products in self.get_all_purchases().customers_and_their_products.items():
            for product in products:
                category_customer_count[product.category][customer] += 1

        return {
            category: [c for c, count in customer_count.items() if count == max(customer_count.values())]
            for category, customer_count in category_customer_count.items()
        }

    def can_customer_pay(self, customer_id: int) -> bool:
        """
        Checks whether a customer with the given ID has enough cash to pay for their purchases.

        :param customer_id: The ID of the customer to check.
        :return: True if the customer’s debt is zero or less (i.e., they can pay), otherwise False.
        """
        return True if self.get_customers_debt(customer_id) == 0 else False

    def get_customers_debt(self, customer_id: int) -> Decimal:
        """
        Calculates the total debt for a customer with the given ID.

        :param customer_id: The ID of the customer whose debt is to be calculated.
        :return: The amount of debt the customer has.
        Returns -1 if the customer does not exist.
        Returns 0 if the customer’s total spending is less than or equal to their cash.
        """
        customer = next((c for c in self.customer_product_repository.get_purchases().customers_and_their_products
                         if customer_id == c.id), None)

        return Decimal(-1) if not customer else max(self.get_customers_total_spent(customer_id) - customer.cash, Decimal(0))

    def get_customers_with_debts(self) -> dict[int, Decimal]:
        """
        Gets a dictionary of customers with the amount of debt they owe.

        :return: A dictionary where the key is a customer's id  and the value is the amount of debt they owe.
        Customers with no debt are not included in the dictionary.

        """
        return {
            customer.id: debt
            for customer, products in self.get_all_purchases().customers_and_their_products.items()
            if (debt := self.get_customers_debt(customer_id=customer.id)) > Decimal(0)
        }

    def _get_unique_products(self) -> dict[int, Product]:
        """
        Retrieves all unique products across all customers.

        :return: A dictionary where the key is the product ID and the value is the `Product` object.
        Each product ID is unique in the dictionary.
        """
        all_products = [p for products in self.get_all_purchases().customers_and_their_products.values()
                        for p in products]
        return {p.id: p for p in all_products}



