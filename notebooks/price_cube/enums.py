from enum import Enum


class BaseEnum(str, Enum):
    """
    BaseEnum is a custom base class for enumerations in the project, inheriting from both `str` and `Enum`.
    It provides additional utility methods for working with enumeration members.

    Methods:
        choices() -> List[str]:
            Returns a list of all the values of the enumeration members.

        names() -> List[str]:
            Returns a list of all the names of the enumeration members.
    """

    @classmethod
    def choices(cls):
        """Return a list of all enum members."""
        return [member.value for member in cls]

    @classmethod
    def names(cls):
        """Return a list of all enum member names."""
        return [member.name for member in cls]


class Category(BaseEnum):
    """
    Category is an enumeration that represents various product categories.

    Attributes:
        ELECTRONICS (str): Represents the "Electronics" category.
        APPAREL (str): Represents the "Apparel" category.
        HOME_KITCHEN (str): Represents the "Home & Kitchen" category.
        SPORTS_OUTDOORS (str): Represents the "Sports & Outdoors" category.
        BEAUTY_HEALTH (str): Represents the "Beauty & Health" category.
    """

    ELECTRONICS = "Electronics"
    APPAREL = "Apparel"
    HOME_KITCHEN = "Home & Kitchen"
    SPORTS_OUTDOORS = "Sports & Outdoors"
    BEAUTY_HEALTH = "Beauty & Health"


class Column(BaseEnum):
    """
    Enum class representing various column names used in the price cube dataset.
    Attributes:
        SKU (str): Represents the stock keeping unit identifier.
        UNIT_COST (str): Represents the unit cost of a product.
        CURRENT_PRICE (str): Represents the current price of a product.
        SUGGESTED_PRICE (str): Represents the suggested price of a product.
        PRODUCT_CATEGORY (str): Represents the category to which a product belongs.
        ELASTICITY (str): Represents the price elasticity of a product.
        DATE (str): Represents the date associated with the data entry.
        PRODUCT_NAME (str): Represents the name of a product.
        PRODUCT_DESCRIPTION (str): Represents the description of a product.
    """

    SKU = "sku"
    UNIT_COST = "unit_cost"
    CURRENT_PRICE = "current_price"
    SUGGESTED_PRICE = "suggested_price"
    PRODUCT_CATEGORY = "product_category"
    ELASTICITY = "elasticity"
    DATE = "date"
    PRODUCT_NAME = "product_name"
    PRODUCT_DESCRIPTION = "product_description"
    UNITS_SOLD = "units_sold"
