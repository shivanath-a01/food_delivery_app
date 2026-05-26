from pydantic import BaseModel
from app.schemas.item_schema import FoodItemResponse

class CartCreate(BaseModel):

    food_item_id: int

    quantity: int

class CartItemResponse(BaseModel):

    id: int

    quantity: int

    unit_price: float

    total_price: float

    food_item: FoodItemResponse

    class Config:
        orm_mode = True
from typing import List

class CartResponse(BaseModel):

    cart_items: List[CartItemResponse]

    grand_total: float

class CartQuantityUpdate(BaseModel):

    quantity: int
