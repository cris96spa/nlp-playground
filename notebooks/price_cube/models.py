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
