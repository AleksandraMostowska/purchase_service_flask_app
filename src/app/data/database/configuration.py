from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models.

    This class is used as a base class for all SQLAlchemy models, enabling them to be mapped to the database.
    """
    pass


# Initialize SQLAlchemy with the custom base class
sa = SQLAlchemy(model_class=Base)
