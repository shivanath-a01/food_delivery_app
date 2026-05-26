from pydantic import BaseModel
from typing import Optional

class FoodItemCreate(BaseModel):

    item_name: str

    description: str

    price: float

    restaurant_id: int
    image_url: Optional[str] = None


class FoodItemResponse(BaseModel):

    id: int
    item_name: str
    description: str
    price: float
    restaurant_id: int
    image_url: Optional[str] = None


    class Config:
        orm_mode = True

 
           