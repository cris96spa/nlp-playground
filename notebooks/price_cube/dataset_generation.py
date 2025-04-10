import os
import random
from datetime import datetime, timedelta
from typing import Any

import numpy as np
import pandas as pd
import polars as pl

from notebooks.price_cube.constants import (
    CATEGORIES,
    DATA_PATH,
    N_ROWS,
    PRODUCT_CATALOG,
    PRODUCT_COSTS,
    PRODUCT_PRICE_RANGES,
    PRODUCTS_PATH,
    ROUND,
    SEED,
)
from notebooks.price_cube.enums import Column
from notebooks.price_cube.environment import Environment
from notebooks.price_cube.utils import (
    build_product_catalog,
    build_product_dict,
    derive_all_metrics,
    generate_random_date,
)

env = Environment()

# Set seed for reproducibility
np.random.seed(SEED)
random.seed(SEED)

# Configuration
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)


category_list = list(CATEGORIES.keys())


# Generate the dataset
product_rows = build_product_catalog(PRODUCT_CATALOG)
product_dict = build_product_dict(product_rows)

skus: list[str] = list(product_dict.keys())
data = []

# Build the dataset
for i in range(N_ROWS):
    # Randomly select a product
    sku = random.choice(skus)
    category = product_dict[sku][Column.PRODUCT_CATEGORY.value]
    product_name = product_dict[sku][Column.PRODUCT_NAME.value]
    product_description = product_dict[sku][Column.PRODUCT_DESCRIPTION.value]

    min_price, max_price = PRODUCT_PRICE_RANGES[sku]

    unit_cost = PRODUCT_COSTS[sku]
    current_price = round(np.random.uniform(min_price, max_price), 2)

    suggested_price = current_price

    # Random date
    date = generate_random_date(start_date, end_date, 1)[0]

    data.append(
        {
            Column.SKU.value: sku,
            Column.UNIT_COST.value: unit_cost,
            Column.CURRENT_PRICE.value: current_price,
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
)

df = derive_all_metrics(df, ROUND).sort(pl.col(Column.DATE.value))

# Save to results

df.write_parquet(
    DATA_PATH + ".parquet",
)
df.write_csv(
    DATA_PATH + ".csv",
)


# Preview
print(df.head())


products_df = (
    df.select(
        [
            pl.col(Column.SKU.value),
            pl.col(Column.PRODUCT_NAME.value),
            pl.col(Column.PRODUCT_CATEGORY.value),
            pl.col(Column.UNIT_COST.value),
            pl.col(Column.PRODUCT_DESCRIPTION.value),
        ]
    )
    .unique()
    .sort(pl.col(Column.PRODUCT_NAME.value))
)

products_df.write_parquet(
    PRODUCTS_PATH + ".parquet",
)
products_df.write_csv(
    PRODUCTS_PATH + ".csv",
)
