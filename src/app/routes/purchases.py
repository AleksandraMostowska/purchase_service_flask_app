from flask import jsonify, Response, Blueprint
import logging
from src.app.configuration import purchase_service
from flask_restful import Resource

logging.basicConfig(level=logging.INFO)


class DataResource(Resource):
    """
    Resource class for handling requests related to purchase data.

    This class uses Flask-RESTful to define an API resource for retrieving purchase data.
    """

    def get(self) -> Response:
        """
        Handles GET requests to retrieve purchase data.

        :return: A JSON response containing the purchase data if available, or a message indicating no data is available.
        """
        data = purchase_service.get_all_purchases()
        if data:
            return {'purchases': data.to_dict()}, 200
        return {'message': 'No SQL data available'}, 500


purchases_blueprint = Blueprint('purchases', __name__, url_prefix='/purchases')


@purchases_blueprint.route('/total_spent/<int:id>', methods=['GET'])
def get_customers_total_spent(id: int) -> Response:
    """
    Returns the total amount spent by a customer with the given ID.

    :param id: The ID of the customer.
    :return: JSON response with total spent amount.
    """

    total_spent = purchase_service.get_customers_total_spent(id)
    return jsonify({'total_spent': float(total_spent)}), 200


@purchases_blueprint.route('/most_spending', methods=['GET'])
def get_customers_who_spent_most() -> Response:
    """
    Returns the customer(s) who have spent the most across all categories.

    :return: JSON response with the list of customers who spent the most.
    """

    top_spenders = purchase_service.get_customer_who_spent_the_most()
    return jsonify({'top_spenders': [customer.to_dict() for customer in top_spenders]}), 200


@purchases_blueprint.route('/most_spending_in_category/<string:category>', methods=['GET'])
def get_most_spending_in_category(category: str) -> Response:
    """
    Returns the customer(s) who have spent the most in a specific category.

    :param category: The product category to check.
    :return: JSON response with the list of customers who spent the most in the category.
    """

    top_spenders = purchase_service.get_most_spending_in_category(category)
    return jsonify({'top_spenders': [customer.to_dict() for customer in top_spenders]}), 200


@purchases_blueprint.route('/age_category_preference', methods=['GET'])
def get_age_category_preference() -> Response:
    """
    Returns a summary of age groups and their most frequently purchased product categories.

    :return: JSON response with the age-category preferences.
    """

    return jsonify({'age_category_preference': purchase_service.get_age_category_preference()}), 200


@purchases_blueprint.route('/category_avg_price', methods=['GET'])
def get_category_and_avg_price() -> Response:
    """
    Returns the average price of products in each category.

    :return: JSON response with category average prices.
    """

    return jsonify({'category_avg_price': purchase_service.get_category_and_avg_price()}), 200


@purchases_blueprint.route('/most_and_least_expensive', methods=['GET'])
def get_most_and_least_expensive_in_category() -> Response:
    """
    Returns the most and least expensive products in each category.

    :return: JSON response with most and least expensive products.
    """

    return jsonify({'most_and_least_expensive': purchase_service.get_most_and_least_expensive_in_category()}), 200


@purchases_blueprint.route('/most_frequent_category', methods=['GET'])
def get_most_frequent_category_for_customers() -> Response:
    """
    Returns the most frequently purchased product category for each customer.

    :return: JSON response with most frequently purchased categories.
    """

    return jsonify(
        {'most_frequent_category_for_customer': purchase_service.get_most_frequent_category_for_customers()}), 200


@purchases_blueprint.route('/can_pay/<int:customer_id>', methods=['GET'])
def can_customer_pay(customer_id: int) -> Response:
    """
    Checks whether a customer with the given ID has enough cash to pay for their purchases.

    :param customer_id: The ID of the customer.
    :return: JSON response indicating if the customer can pay or not.
    """

    return jsonify({'can_pay': purchase_service.can_customer_pay(customer_id)}), 200


@purchases_blueprint.route('/get_debt/<int:customer_id>', methods=['GET'])
def get_customers_debt(customer_id: int) -> Response:
    """
    Returns the total debt for a customer with the given ID.

    :param customer_id: The ID of the customer.
    :return: JSON response with the customer's debt or an error message.
    """

    return jsonify({'debt': purchase_service.get_customers_debt(customer_id)}), 200


@purchases_blueprint.route('/indebted_customers', methods=['GET'])
def get_customers_with_debts() -> Response:
    """
    Returns a dictionary of customers with the amount of debt they owe.

    :param source: The data source type ('csv', 'json', 'sql').
    :return: JSON response with customers and their debts.
    """

    return jsonify({'indebted_customers': purchase_service.get_customers_with_debts()}), 200
