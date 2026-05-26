from pydantic import BaseModel
from app.schemas.item_schema import FoodItemResponse
from typing import List


class RestaurantCreate(BaseModel):

    restaurant_name: str

    restaurant_address: str

    contact_phone: str

class RestaurantResponse(BaseModel):

    id: int
    restaurant_name: str
    restaurant_address: str
    contact_phone: str

    food_items: List[FoodItemResponse]

    class Config:
        orm_mode = True
        
           