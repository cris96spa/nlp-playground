import os
import random
from datetime import datetime, timedelta
from typing import Any

import numpy as np
import pandas as pd
import polars as pl

from notebooks.price_cube.constants import (
    CATEGORIES,
    ELASTICITY,
    N_ROWS,
    PRODUCT_CATALOG,
    PRODUCT_PRICE_RANGES,
    SEED,
)
from notebooks.price_cube.enums import Category, Column


# Add this at the top of your script
class Environment:
    def __init__(self, scale: int | None = None):
        self.scale = scale if scale is not None else 1
        np.random.seed(42)

    def demand(self, x: np.ndarray) -> np.ndarray:
        return self.scale * np.exp(-((2 * x) ** 2))

    def objective_function(
        self, x: np.ndarray, y: np.ndarray, ly_x=0, lx_y=0
    ) -> np.ndarray:
        return x * self.demand_x(x, y, ly_x) + y * self.demand_x(y, x, lx_y)

    def demand_x(self, x: np.ndarray, y: np.ndarray, l=0) -> np.ndarray:
        return self.demand(x) + l * self.demand(y)

    def sample(self, X, noise=True):
        if noise:
            noise = np.random.normal(0, self.scale * 0.1, X[0].shape)
        else:
            noise = 0
        return self.objective_function(X[0], X[1]) + noise

    def sample_demand_x(self, X, noise=True, l=0):
        if noise:
            noise = np.random.normal(0, self.scale * 0.1, X[0].shape)
        else:
            noise = 0
        return self.demand_x(X[0], X[1], l=l) + noise


env = Environment()

# Set seed for reproducibility
np.random.seed(SEED)
random.seed(SEED)

# Configuration
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)


category_list = list(CATEGORIES.keys())

DATASET_PATH = os.path.join("notebooks", "price_cube", "dataset", "price_cube.parquet")


# Generate random date
def generate_random_date(start, end, n):
    return [
        start + timedelta(days=random.randint(0, (end - start).days)) for _ in range(n)
    ]


# Price elasticity: higher means more price sensitive
def sample_elasticity(category: str, elasticity: dict):
    return np.random.normal(elasticity[category], 0.2)


def build_product_catalog(catalog: dict) -> list[dict]:
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
    product_dict = {}
    for product in product_list:
        product_dict[product[Column.SKU.value]] = product
    return product_dict


def generate_units_sold_env(current_price):
    # Normalize price to [0, 1] scale roughly (based on assumed max price)
    norm_price = np.array([current_price / 500])  # Assume max price ~500
    dummy_y = np.array([0])
    demand = env.sample_demand_x((norm_price, dummy_y), noise=True, l=0)[0]

    # Scale demand to a plausible units sold number
    units = int(max(1, demand * 100 + np.random.normal(0, 3)))  # scale + noise
    return units


# Generate the dataset
product_rows = build_product_catalog(PRODUCT_CATALOG)
product_dict = build_product_dict(product_rows)

skus: list[str] = list(product_dict.keys())
data = []

for i in range(N_ROWS):
    sku = random.choice(skus)
    category = product_dict[sku][Column.PRODUCT_CATEGORY.value]
    product_name = product_dict[sku][Column.PRODUCT_NAME.value]
    product_description = product_dict[sku][Column.PRODUCT_DESCRIPTION.value]

    cost_min, cost_max = PRODUCT_PRICE_RANGES[sku]

    unit_cost = round(np.random.uniform(cost_min, cost_max), 2)
    current_price = round(unit_cost * np.random.uniform(1.2, 1.8), 2)
    elasticity = sample_elasticity(category=category, elasticity=ELASTICITY)
    units_sold = generate_units_sold_env(current_price)

    # Simulate a price suggestion: optimize margin with elasticity
    margin_boost = np.clip(1 + (-elasticity * 0.05), 1.05, 1.3)
    suggested_price = round(unit_cost * margin_boost, 2)

    # Random date
    date = generate_random_date(start_date, end_date, 1)[0]

    data.append(
        {
            Column.SKU.value: sku,
            Column.UNIT_COST.value: unit_cost,
            Column.CURRENT_PRICE.value: current_price,
            Column.UNITS_SOLD.value: units_sold,
            Column.SUGGESTED_PRICE.value: suggested_price,
            Column.PRODUCT_CATEGORY.value: category,
            Column.DATE.value: date,
            Column.PRODUCT_NAME.value: product_name,
            Column.PRODUCT_DESCRIPTION.value: product_description,
        }
    )

# Create DataFrame
df = pl.DataFrame(
    data,
).sort(pl.col(Column.DATE.value))


# Save to CSV if needed
df.write_parquet(
    DATASET_PATH,
)

# Preview
print(df.head())
