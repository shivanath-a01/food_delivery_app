from pydantic import BaseModel


class RestaurantRegister(BaseModel):

    restaurant_name: str

    restaurant_address: str

    contact_phone: str

    email: str

    password: str


class RestaurantLogin(BaseModel):

    email: str

    password: str