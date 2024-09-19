import os
from pathlib import Path
import requests
from flask import Flask, jsonify
from flask_restful import Api
import logging
from src.app.routes.purchases import purchases_blueprint
from src.app.data.database.configuration import sa
from dotenv import load_dotenv
from src.app.routes.purchases import DataResource

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)


def main() -> Flask:
    """
    Main function to set up and run the Flask application.

    This function:
    - Loads environment variables from a .env file.
    - Configures the SQLAlchemy database URI using an environment variable.
    - Initializes SQLAlchemy with the Flask application.
    - Defines error handling for the application.
    - Registers routes and blueprints.
    - Returns the configured Flask application instance.
    """
    with app.app_context():
        # Load environment variables from the .env file
        ENV_FILENAME = '.env'
        ENV_PATH = Path(__file__).resolve().parent.parent.parent / ENV_FILENAME
        load_dotenv(ENV_PATH)

        # Configure SQLAlchemy with the database URI
        app.config['SQLALCHEMY_DATABASE_URI'] = requests.get(os.getenv('SQLALCHEMY_DATABASE_URL')).text.strip()
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        sa.init_app(app)

        # Define error handler for the application
        @app.errorhandler(Exception)
        def handle_error(error: Exception):
            """
            Error handler for exceptions.

            :param error: The exception that was raised.
            :return: A JSON response containing the error message and a 500 status code.
            """
            error_message = error.args[0]
            return {'message': error_message}, 500

        # Define a test route to raise an error
        @app.route('/error_test')
        def error_test():
            """
            Test route to trigger a ValueError for testing purposes.

            :return: A JSON response containing a test error message.
            """
            if 1 == 1:
                raise ValueError('Test error')

        # Define a route to return author information
        @app.route('/author')
        def get_purchases():
            """
            Route to get author information.

            :return: A JSON response containing author information and version.
            """
            return jsonify({
                'author': 'AM',
                'version': 1.0
            })

        # Define a route to log paths and return author information
        @app.route('/fake')
        def fake_route():
            """
            Route to log CSV and JSON paths and return author information.

            :return: A JSON response containing author information and version.
            """
            logging.info(f"CSV_PATH: {os.getenv('CSV_PATH')}")
            logging.info(f"JSON_PATH: {os.getenv('JSON_PATH')}")

            return jsonify({
                'author': 'AM',
                'version': 1.0
            })

        # Initialize Flask-RESTful API and add resources
        api = Api(app)
        api.add_resource(DataResource, '/data')

        # Register the purchases blueprint
        app.register_blueprint(purchases_blueprint)

        return app