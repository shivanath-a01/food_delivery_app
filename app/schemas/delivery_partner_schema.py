from pydantic import BaseModel, EmailStr


class DeliveryPartnerCreate(BaseModel):

    name: str

    email: EmailStr

    password: str

    phone: str

    vehicle_type: str

    vehicle_number: str

    license_number: str



class DeliveryPartnerLogin(BaseModel):

    email: EmailStr

    password: str