import random
from datetime import datetime, timedelta
from typing import Any

import numpy as np
import polars as pl
from scipy.optimize import minimize_scalar

from notebooks.price_cube.constants import (
    MAX_UNITS_SOLD,
    PRODUCT_PRICE_RANGES_CONSTRAINTS,
)
from notebooks.price_cube.enums import Column


@np.vectorize
def logistic_decay(prices: np.ndarray, L: float, k: float, p0: float) -> np.ndarray:
    """
    Logistic decay function for smoothing demand.

    Parameters:
        prices (np.ndarray): Prices.
        L (float): Maximum units sold.
        k (float): Steepness of the curve.
        p0 (float): Price at inflection point.

    Returns:
        np.ndarray: Smoothed units sold.
    """
    return L / (1 + np.exp(k * (prices - p0)))


def margin_volume_objective(price, cost, L, k, p0):
    """
    Computes the negative margin-volume objective for a given price, cost, and logistic decay parameters.

    This function calculates the product of the margin and the volume, where the volume is determined
    using a logistic decay function. The result is negated to facilitate maximization in optimization
    problems. Pricing below cost is penalized by returning infinity.

    Parameters:
        price (float): The price of the product.
        cost (float): The cost of the product.
        L (float): The logistic decay parameter representing the maximum volume.
        k (float): The logistic decay steepness parameter.
        p0 (float): The logistic decay midpoint parameter.

    Returns:
        float: The negative margin-volume objective. Returns np.inf if price is less than or equal to cost.
    """

    if price <= cost:
        return np.inf  # don't allow pricing below cost
    volume = logistic_decay(np.array([price]), L, k, p0)[0]
    margin = (price - cost) / cost
    return -margin * volume  # negative for maximization


def find_optimal_price(cost, L, k, p0, price_bounds=(0.0, 1e6)):
    """
    Finds the optimal price that maximizes the margin-volume tradeoff for a product.

    This function uses a scalar minimization algorithm to determine the price
    that optimizes the margin-volume objective function, given the cost of the
    product, demand parameters, and initial price.

    Args:
        cost (float): The cost of producing the product.
        L (float): The maximum potential demand for the product.
        k (float): The price sensitivity parameter.
        p0 (float): The reference price for the product.
        price_bounds (tuple, optional): A tuple specifying the lower and upper
            bounds for the price search. Defaults to (0.01, 10.0).

    Returns:
        float or None: The optimal price if the optimization is successful,
        otherwise None.
    """
    result = minimize_scalar(
        margin_volume_objective,
        bounds=price_bounds,
        args=(cost, L, k, p0),
        method="bounded",
    )
    return result.x if result.success else None  # type: ignore[return-value] # pragma: no cover


# Generate random date
def generate_random_date(start: datetime, end: datetime, n: int):
    """
    Generate a list of random dates within a specified range.

    Args:
        start (datetime): The start date of the range.
        end (datetime): The end date of the range.
        n (int): The number of random dates to generate.

    Returns:
        list[datetime]: A list containing `n` random dates between `start` and `end`.
    """
    return [
        start + timedelta(days=random.randint(0, (end - start).days)) for _ in range(n)
    ]


def build_product_catalog(catalog: dict) -> list[dict]:
    """
    Builds a product catalog as a list of dictionaries from the given catalog data.

    Args:
        catalog (dict): A dictionary where the keys represent product categories and
                        the values are lists of tuples. Each tuple contains the SKU,
                        product name, and product description.

    Returns:
        list[dict]: A list of dictionaries where each dictionary represents a product
                    with the following keys:
                    - 'SKU': The stock keeping unit of the product.
                    - 'PRODUCT_CATEGORY': The category of the product.
                    - 'PRODUCT_NAME': The name of the product.
                    - 'PRODUCT_DESCRIPTION': The description of the product.

    Example:
        catalog = {
            "Electronics": [
                ("12345", "Smartphone", "A high-end smartphone"),
                ("67890", "Laptop", "A powerful laptop"),
            ],
            "Books": [
                ("54321", "Fiction Book", "A thrilling fiction novel"),
            ],
        result = build_product_catalog(catalog)
        # result will be:
        # [
        #     {
        #         'SKU': '12345',
        #         'PRODUCT_CATEGORY': 'Electronics',
        #         'PRODUCT_NAME': 'Smartphone',
        #         'PRODUCT_DESCRIPTION': 'A high-end smartphone',
        #     },
        #     {
        #         'SKU': '67890',
        #         'PRODUCT_CATEGORY': 'Electronics',
        #         'PRODUCT_NAME': 'Laptop',
        #         'PRODUCT_DESCRIPTION': 'A powerful laptop',
        #     },
        #     {
        #         'SKU': '54321',
        #         'PRODUCT_CATEGORY': 'Books',
        #         'PRODUCT_NAME': 'Fiction Book',
        #         'PRODUCT_DESCRIPTION': 'A thrilling fiction novel',
        #     },
        # ]
    """
    product_rows = []
    for category, products in catalog.items():
        for sku, product_name, description in products:
            product_rows.append(
                {
                    Column.SKU.value: sku,
                    Column.PRODUCT_CATEGORY.value: category,
                    Column.PRODUCT_NAME.value: product_name,
                    Column.PRODUCT_DESCRIPTION.value: description,
                }
            )
    return product_rows


def build_product_dict(product_list: list) -> dict[str, Any]:
    """
    Constructs a dictionary mapping product SKUs to their corresponding product data.

    Args:
        product_list (list): A list of product data, where each product is represented
                             as a dictionary or object containing a SKU field.

    Returns:
        dict[str, Any]: A dictionary where the keys are SKUs (as strings) and the values
                        are the corresponding product data.

    Raises:
        KeyError: If a product in the list does not contain the SKU field.
    """
    product_dict = {}
    for product in product_list:
        product_dict[product[Column.SKU.value]] = product
    return product_dict


def derive_volume_metrics(df: pl.DataFrame, _round: bool = False) -> pl.DataFrame:
    """
    Generate volume-related metrics for products in a given DataFrame.
    This function calculates various metrics such as units sold, expected volume,
    minimum price, maximum price, and suggested price for each product in the
    input DataFrame. It uses logistic decay to model expected demand and introduces
    noise to simulate real-world variability. Additionally, it determines the optimal
    price for each product based on cost and price constraints.
    Args:
        df (pl.DataFrame): Input DataFrame containing product data. It must include
            columns for SKU, current price, and unit cost.
    Returns:
        pl.DataFrame: A new DataFrame with the original data sorted by SKU and
        current price, along with additional columns:
            - UNITS_SOLD: Simulated units sold for each product.
            - EXPECTED_units_sold: Expected demand volume based on logistic decay.
            - MIN_PRICE: Minimum price constraint for each product.
            - MAX_PRICE: Maximum price constraint for each product.
            - SUGGESTED_PRICE: Suggested optimal price for each product.
    Notes:
        - The function assumes the existence of global variables:
            - MAX_UNITS_SOLD: A dictionary mapping product IDs to their maximum
              units sold.
            - PRODUCT_PRICE_RANGES_CONSTRAINTS: A dictionary mapping product IDs
              to their price range constraints.
        - The `logistic_decay` and `find_optimal_price` functions are used to
          compute expected demand and optimal price, respectively.
        - Noise is introduced to the expected volume to simulate real-world
          variability in demand.
    """

    units_sold_list = []
    expected_units_sold_list = []
    optimal_units_sold_list = []
    min_price_list = []
    max_price_list = []
    suggested_price_list = []
    global_optimal_price_list = []
    current_prices_list = []
    for product_id in df[Column.SKU.value].unique().sort().to_numpy():
        # Filter products by SKU
        print(f"Product ID: {product_id}")
        products = df.filter(pl.col(Column.SKU.value) == product_id).sort(
            pl.col(Column.CURRENT_PRICE.value)
        )

        # Get the cost of the current product. It is the same for each row
        cost = products[Column.UNIT_COST.value][0]

        # Get the historical selling prices
        current_prices = products[Column.CURRENT_PRICE.value].to_numpy()

        # Setup logistic decay parameters
        L = MAX_UNITS_SOLD[product_id]

        k = np.random.uniform(5, 10) / (
            np.max(current_prices) - np.min(current_prices)
        )  # Dynamic steepness
        p0 = np.median(current_prices)

        # Compute expected units sold using logistic decay
        units_sold = logistic_decay(current_prices, L=L, k=k, p0=p0)

        # Get the optimal price
        price_bounds = PRODUCT_PRICE_RANGES_CONSTRAINTS[product_id]
        suggested_price = find_optimal_price(cost, L, k, p0, price_bounds=price_bounds)
        global_optimal_price = find_optimal_price(
            cost,
            L,
            k,
            p0,
            price_bounds=(np.min(current_prices), np.max(current_prices)),
        )

        expected_units_sold = logistic_decay(suggested_price, L=L, k=k, p0=p0)
        optimal_units_sold = logistic_decay(global_optimal_price, L=L, k=k, p0=p0)

        if _round:
            units_sold = np.round(units_sold)
            expected_units_sold = np.round(expected_units_sold)
            optimal_units_sold = np.round(optimal_units_sold)

        # Save results of current product
        units_sold_list.extend(units_sold.tolist())
        expected_units_sold_list.extend(
            np.repeat(expected_units_sold, len(units_sold)).tolist()
        )
        optimal_units_sold_list.extend(
            np.repeat(optimal_units_sold, len(units_sold)).tolist()
        )
        min_price_list.extend([price_bounds[0]] * len(units_sold))
        max_price_list.extend([price_bounds[1]] * len(units_sold))
        suggested_price_list.extend([suggested_price] * len(units_sold))
        global_optimal_price_list.extend([global_optimal_price] * len(units_sold))
        current_prices_list.extend(current_prices.tolist())

    return df.sort([Column.SKU.value, Column.CURRENT_PRICE.value]).with_columns(
        [
            pl.Series(Column.UNITS_SOLD.value, units_sold_list).alias(
                Column.UNITS_SOLD.value
            ),
            pl.Series(Column.EXPECTED_UNITS_SOLD.value, expected_units_sold_list).alias(
                Column.EXPECTED_UNITS_SOLD.value
            ),
            pl.Series(Column.OPTIMAL_UNITS_SOLD.value, optimal_units_sold_list).alias(
                Column.OPTIMAL_UNITS_SOLD.value
            ),
            pl.Series(Column.MIN_PRICE.value, min_price_list).alias(
                Column.MIN_PRICE.value
            ),
            pl.Series(Column.MAX_PRICE.value, max_price_list).alias(
                Column.MAX_PRICE.value
            ),
            pl.Series(Column.SUGGESTED_PRICE.value, suggested_price_list).alias(
                Column.SUGGESTED_PRICE.value
            ),
            pl.Series(
                Column.GLOBAL_OPTIMAL_PRICE.value, global_optimal_price_list
            ).alias(Column.GLOBAL_OPTIMAL_PRICE.value),
            pl.Series(Column.CURRENT_PRICE.value, current_prices_list).alias(
                Column.CURRENT_PRICE.value
            ),
        ]
    )


def derive_margin_metrics(df: pl.DataFrame) -> pl.DataFrame:
    """
    Calculate margin-related metrics for a given DataFrame.

    Args:
        df (pl.DataFrame): Input DataFrame containing product data. It must include
            columns for SKU, unit cost, current price, and suggested price.

    Returns:
        pl.DataFrame: A new DataFrame with the original data sorted by SKU and
        current price, along with additional columns:
            - MARGIN: The margin for each product based on the current price.
            - SUGGESTED_MARGIN: The suggested margin for each product based on
              the suggested price.
    """
    return df.with_columns(
        [
            (
                (pl.col(Column.CURRENT_PRICE.value) - pl.col(Column.UNIT_COST.value))
                / pl.col(Column.UNIT_COST.value)
            ).alias(Column.CURRENT_MARGIN_PERCENTAGE.value),
            (
                (pl.col(Column.SUGGESTED_PRICE.value) - pl.col(Column.UNIT_COST.value))
                / pl.col(Column.UNIT_COST.value)
            ).alias(Column.SUGGESTED_MARGIN_PERCENTAGE.value),
            (
                (
                    pl.col(Column.GLOBAL_OPTIMAL_PRICE.value)
                    - pl.col(Column.UNIT_COST.value)
                )
                / pl.col(Column.UNIT_COST.value)
            ).alias(Column.OPTIMAL_MARGIN_PERCENTAGE.value),
            (
                (pl.col(Column.CURRENT_PRICE.value) - pl.col(Column.UNIT_COST.value))
                * pl.col(Column.UNITS_SOLD.value)
            ).alias(Column.CURRENT_NET_MARGIN.value),
            (
                (pl.col(Column.SUGGESTED_PRICE.value) - pl.col(Column.UNIT_COST.value))
                * pl.col(Column.EXPECTED_UNITS_SOLD.value)
            ).alias(Column.EXPECTED_NET_MARGIN_EXPECTED_VOLUME.value),
            (
                (
                    pl.col(Column.GLOBAL_OPTIMAL_PRICE.value)
                    - pl.col(Column.UNIT_COST.value)
                )
                * pl.col(Column.OPTIMAL_UNITS_SOLD.value)
            ).alias(Column.OPTIMAL_NET_MARGIN.value),
        ]
    )


def derive_revenue_metrics(df: pl.DataFrame) -> pl.DataFrame:
    """
    Derives revenue-related metrics for a given DataFrame.

    This function calculates and adds the following columns to the input DataFrame:
    - `CURRENT_REVENUE`: The revenue based on the current price and units sold.
    - `EXPECTED_REVENUE_CURRENT_VOLUME`: The expected revenue based on the suggested price and current volume of units sold.
    - `EXPECTED_REVENUE_EXPECTED_VOLUME`: The expected revenue based on the suggested price and expected volume of units sold.

    Args:
        df (pl.DataFrame): The input DataFrame containing the necessary columns for calculations.

    Returns:
        pl.DataFrame: A new DataFrame with the derived revenue metrics added as columns.

    Required Columns in `df`:
        - `Column.CURRENT_PRICE.value`: The current price of the product.
        - `Column.UNITS_SOLD.value`: The number of units sold.
        - `Column.SUGGESTED_PRICE.value`: The suggested price of the product.
        - `Column.EXPECTED_UNITS_SOLD.value`: The expected number of units to be sold.
    """

    return df.with_columns(
        [
            (
                pl.col(Column.CURRENT_PRICE.value) * pl.col(Column.UNITS_SOLD.value)
            ).alias(Column.CURRENT_REVENUE.value),
            (
                pl.col(Column.SUGGESTED_PRICE.value)
                * pl.col(Column.EXPECTED_UNITS_SOLD.value)
            ).alias(Column.EXPECTED_REVENUE_EXPECTED_VOLUME.value),
            (
                pl.col(Column.GLOBAL_OPTIMAL_PRICE.value)
                * pl.col(Column.OPTIMAL_UNITS_SOLD.value)
            ).alias(Column.OPTIMAL_REVENUE.value),
        ]
    )


def derive_all_metrics(df: pl.DataFrame, _round=True) -> pl.DataFrame:
    """
    Calculate all relevant metrics for a given DataFrame.

    Args:
        df (pl.DataFrame): Input DataFrame containing product data. It must include
            columns for SKU, unit cost, current price, and suggested price.

    Returns:
        pl.DataFrame: A new DataFrame with the original data sorted by SKU and
        current price, along with additional columns for margin and revenue metrics.
    """
    df = derive_volume_metrics(df, _round=_round)
    df = derive_margin_metrics(df)
    df = derive_revenue_metrics(df)
    return df
