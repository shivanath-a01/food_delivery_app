from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.customer_schema import CustomerLogin
from app.auth.hash import verify_password
from app.auth.token import create_access_token
from fastapi import HTTPException
from app.auth.token import get_current_user
from fastapi.security import OAuth2PasswordRequestForm



from app.schemas.customer_schema import CustomerCreate
from app.models.customer import Customer
from app.deps import get_db
from app.auth.hash import hash_password

router = APIRouter()

@router.post("/register")
def register_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    
    new_customer = Customer(
        customer_name=customer.customer_name,
        contact_phone=customer.contact_phone,
        email=customer.email,
        password=hash_password(customer.password)
    )

    db.add(new_customer)

    db.commit()

    db.refresh(new_customer)

    return {
        "message": "Customer registered successfully"
    }

@router.post("/login")
def login_customer(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    existing_customer = db.query(Customer).filter(
        Customer.email == request.username
    ).first()

    if not existing_customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    password_correct = verify_password(
        request.password,
        existing_customer.password
    )

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = create_access_token(
        data={"sub": existing_customer.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/profile")
def get_profile(
    current_user: Customer = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "customer_name": current_user.customer_name,
        "email": current_user.email,
        "contact_phone": current_user.contact_phone
    }
