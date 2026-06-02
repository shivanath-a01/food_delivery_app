from pydantic import BaseModel, EmailStr

class CustomerCreate(BaseModel):
    customer_name: str
    contact_phone: str
    email: EmailStr
    password: str
    role: str = "customer"
    
class CustomerLogin(BaseModel):
    email: EmailStr
    password: str