from pydantic import BaseModel


class DeliveryPartnerCreate(BaseModel):

    name: str

    phone: str

    vehicle_number: str

