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
    Column is an enumeration that defines various attributes related to product pricing, sales, and performance metrics.

    Attributes:
        SKU (str): The stock-keeping unit identifier for a product.
        DATE (str): The date associated with the data entry.
        PRODUCT_NAME (str): The name of the product.
        PRODUCT_DESCRIPTION (str): A description of the product.
        UNIT_COST (str): The cost per unit of the product.
        PRODUCT_CATEGORY (str): The category to which the product belongs.

        MIN_PRICE (str): The minimum price of the product.
        MAX_PRICE (str): The maximum price of the product.
        CURRENT_PRICE (str): The current price of the product.
        SUGGESTED_PRICE (str): The suggested price for the product.

        GLOBAL_OPTIMAL_PRICE (str): The globally optimal price for the product.

        UNITS_SOLD (str): The number of units sold.
        EXPECTED_UNITS_SOLD (str): The expected number of units to be sold.
        OPTIMAL_UNITS_SOLD (str): The optimal number of units to be sold.

        CURRENT_MARGIN_PERCENTAGE (str): The current profit margin percentage.
        SUGGESTED_MARGIN_PERCENTAGE (str): The suggested profit margin percentage.
        OPTIMAL_MARGIN_PERCENTAGE (str): The optimal profit margin percentage.

        CURRENT_REVENUE (str): The current revenue generated.
        EXPECTED_REVENUE_CURRENT_VOLUME (str): The expected revenue based on current sales volume.
        EXPECTED_REVENUE_EXPECTED_VOLUME (str): The expected revenue based on expected sales volume.
        OPTIMAL_REVENUE (str): The optimal revenue that can be achieved.

        CURRENT_NET_MARGIN (str): The current net margin.
        EXPECTED_NET_MARGIN_CURRENT_VOLUME (str): The expected net margin based on current sales volume.
        EXPECTED_NET_MARGIN_EXPECTED_VOLUME (str): The expected net margin based on expected sales volume.
        OPTIMAL_NET_MARGIN (str): The optimal net margin that can be achieved.
    """

    SKU = "sku"
    DATE = "date"
    PRODUCT_NAME = "product_name"
    PRODUCT_DESCRIPTION = "product_description"
    UNIT_COST = "unit_cost"
    PRODUCT_CATEGORY = "product_category"

    MIN_PRICE = "min_price"
    MAX_PRICE = "max_price"
    CURRENT_PRICE = "current_price"
    SUGGESTED_PRICE = "suggested_price"

    GLOBAL_OPTIMAL_PRICE = "global_optimal_price"

    UNITS_SOLD = "units_sold"
    EXPECTED_UNITS_SOLD = "expected_units_sold"
    OPTIMAL_UNITS_SOLD = "optimal_units_sold"

    CURRENT_MARGIN_PERCENTAGE = "current_margin_percentage"
    SUGGESTED_MARGIN_PERCENTAGE = "suggested_margin_percentage"
    OPTIMAL_MARGIN_PERCENTAGE = "optimal_margin_percentage"

    CURRENT_NET_MARGIN = "current_net_margin"
    EXPECTED_NET_MARGIN_EXPECTED_VOLUME = "expected_net_margin_expected_volume"
    OPTIMAL_NET_MARGIN = "optimal_net_margin"

    CURRENT_REVENUE = "current_revenue"
    EXPECTED_REVENUE_EXPECTED_VOLUME = "expected_revenue_expected_volume"
    OPTIMAL_REVENUE = "optimal_revenue"

    COSTS = "costs"
