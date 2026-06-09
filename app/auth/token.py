from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException
from app.models.customer import Customer
from app.models.restaurant import Restaurant

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt
from jose import JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.database import SessionLocal
from app.models.customer import Customer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/restaurant/login"
)

def get_current_user(token: str = Depends(oauth2_scheme)):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token is invalid or expired"
        )

    db = SessionLocal()

    customer = db.query(Customer).filter(
        Customer.email == email
    ).first()

    db.close()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer

def get_current_admin(
    current_user: Customer = Depends(get_current_user)
):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return current_user


def get_current_restaurant(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token is invalid or expired"
        )

    db = SessionLocal()

    restaurant = db.query(
        Restaurant
    ).filter(
        Restaurant.email == email
    ).first()

    db.close()

    if restaurant is None:

        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return restaurant

