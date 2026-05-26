from pydantic import BaseModel

class FoodItemCreate(BaseModel):

    item_name: str

    description: str

    price: float

    restaurant_id: int

class FoodItemResponse(BaseModel):

    id: int
    item_name: str
    description: str
    price: float
    restaurant_id: int

    class Config:
        orm_mode = True

 
           