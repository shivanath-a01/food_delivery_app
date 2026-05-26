from pydantic import BaseModel
from typing import List

class OrderItemResponse(BaseModel):

    food_item_name: str

    quantity: int

    item_price: float

    total_price: float

class OrderResponse(BaseModel):

    order_id: int

    total_amount: float

    status: str

    items: List[OrderItemResponse]

class OrderStatusUpdate(BaseModel):

    status: str

