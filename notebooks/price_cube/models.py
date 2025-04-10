from datetime import datetime

from pydantic import BaseModel, Field


class Point(BaseModel):
    x: float = Field(description="x-coordinate of the point")
    y: float = Field(description="y-coordinate of the point")


class ModalSkuData(BaseModel):
    min_value: Point = Field(
        description="x and y values for the minimum price for constrained optimization"
    )
    max_value: Point = Field(
        description="x and y values for the maximum price for constrained optimization"
    )
    price_x: list[float] = Field(description="Price values for the x-variable")
    volume_y: list[float] = Field(description="Volume values for the y-variable")

    net_margin_y: list[float] = Field(
        description="Net margin values for the y-variable"
    )
    suggested_optimal: Point = Field(
        description="x and y values for the suggested optimal price"
    )
    global_optimal: Point = Field(
        description="x and y values for the global optimal price"
    )
    description: str = Field(
        description="Description of the product, including its features and benefits"
    )


class PricingOptimizationRecap(BaseModel):
    current_revenue: float = Field(
        description="Current revenue generated from product sales"
    )
    expected_revenue: float = Field(
        description="Expected revenue based on current sales volume"
    )
    current_net_margin: float = Field(
        description="Current net margin generated from product sales"
    )
    expected_net_margin: float = Field(
        description="Expected net margin based on current sales volume"
    )


class DashboardPlots(BaseModel):
    dates: list[datetime] = Field(description="Date of the data point")
    costs: list[float] = Field(description="Cost values for the product over time")
    current_revenue: list[float] = Field(
        description="Current revenue generated from product sales"
    )
    expected_revenue: list[float] = Field(
        description="Expected revenue based on current sales volume"
    )
    current_net_margin: list[float] = Field(
        description="Current net margin generated from product sales"
    )
    expected_net_margin: list[float] = Field(
        description="Expected net margin based on current sales volume"
    )
    units_sold: list[float] = Field(description="Units sold for the product over time")
    expected_units_sold: list[float] = Field(
        description="Expected units sold based on current sales volume"
    )
    current_margin_percentage: list[float] = Field(
        description="Net margin percentage for the product over time"
    )
    expected_margin_percentage: list[float] = Field(
        description="Expected net margin percentage based on current sales volume"
    )


class Product(BaseModel):
    sku: str = Field(description="Stock Keeping Unit (SKU) of the product")
    product_name: str = Field(
        description="Name of the product, including its features and benefits"
    )
    product_description: str = Field(
        description="Description of the product, including its features and benefits"
    )
    product_category: str = Field(
        description="Category of the product, including its features and benefits"
    )
    unit_cost: float = Field(
        description="Cost per unit of the product, including its features and benefits"
    )
