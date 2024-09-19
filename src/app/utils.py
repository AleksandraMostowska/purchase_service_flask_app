from dataclasses import dataclass
from src.app.model import Product


@dataclass
class MaxMin:
    """
    Class to store the maximum and minimum priced products within a category.
    """
    max: Product
    min: Product
