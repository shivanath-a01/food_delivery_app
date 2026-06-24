from fastapi import APIRouter, Depends, Query
from app.models.order import Order
from app.models.order import Order
from app.models.restaurant import Restaurant
from app.auth.token import get_current_restaurant
from sqlalchemy.orm import Session
from app.models.item import FoodItem
from passlib.context import CryptContext
from app.auth.token import create_access_token

from app.auth.token import (
    get_current_restaurant
)
from app.schemas.order_schema import (
    OrderStatusUpdate
)
from app.schemas.restaurant_auth_schema import (
    RestaurantRegister,
    RestaurantLogin
)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


from app.schemas.item_schema import FoodItemResponse

from app.models.restaurant import Restaurant
from app.schemas.restaurant_schema import RestaurantCreate
from app.deps import get_db
from app.schemas.restaurant_schema import (
    RestaurantCreate,
    RestaurantResponse
)
from typing import List

from fastapi import HTTPException


router = APIRouter()

@router.post("/restaurants")
def create_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db)
):

    existing_restaurant = db.query(Restaurant).filter(
        Restaurant.restaurant_name ==
        restaurant.restaurant_name
    ).first()

    if existing_restaurant:
        raise HTTPException(
            status_code=400,
            detail="Restaurant already exists"
        )

    new_restaurant = Restaurant(
        restaurant_name=restaurant.restaurant_name,
        restaurant_address=restaurant.restaurant_address,
        contact_phone=restaurant.contact_phone
    )

    db.add(new_restaurant)

    db.commit()

    db.refresh(new_restaurant)

    return {
        "message": "Restaurant created successfully"
    }

@router.post("/restaurant/register")
def register_restaurant(
    restaurant_data: RestaurantRegister,
    db: Session = Depends(get_db)
):

    existing_restaurant = db.query(
        Restaurant
    ).filter(
        Restaurant.email ==
        restaurant_data.email
    ).first()

    if existing_restaurant:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(
        restaurant_data.password
    )

    restaurant = Restaurant(
        restaurant_name=
            restaurant_data.restaurant_name,

        restaurant_address=
            restaurant_data.restaurant_address,

        contact_phone=
            restaurant_data.contact_phone,

        email=
            restaurant_data.email,

        password=
            hashed_password
    )

    db.add(restaurant)

    db.commit()

    db.refresh(restaurant)

    return {
        "message":
            "Restaurant registered successfully"
    }

@router.post("/restaurant/login")
def restaurant_login(
    login_data: RestaurantLogin,
    db: Session = Depends(get_db)
):

    restaurant = db.query(
        Restaurant
    ).filter(
        Restaurant.email ==
        login_data.email
    ).first()

    if not restaurant:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not pwd_context.verify(
        login_data.password,
        restaurant.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": restaurant.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "restaurant_name":
            restaurant.restaurant_name
    }

@router.get("/restaurant/me")
def get_restaurant_profile(

    current_restaurant: Restaurant =
    Depends(get_current_restaurant)

):

    return {
        "id":
            current_restaurant.id,

        "restaurant_name":
            current_restaurant.restaurant_name,

        "restaurant_address":
            current_restaurant.restaurant_address,

        "contact_phone":
            current_restaurant.contact_phone,

        "email":
            current_restaurant.email
    }


@router.get(
    "/restaurants/search",
    response_model=List[RestaurantResponse]
)
def search_restaurants(
    keyword: str = Query(...),
    db: Session = Depends(get_db)
):

    restaurants = db.query(Restaurant).filter(
        Restaurant.restaurant_name.ilike(f"%{keyword}%")
    ).all()

    return restaurants

@router.get(
    "/restaurants/{restaurant_id}/items",
    response_model=List[FoodItemResponse]
)
def get_restaurant_items(
    restaurant_id: int,
    db: Session = Depends(get_db)
):

    items = db.query(FoodItem).filter(
        FoodItem.restaurant_id == restaurant_id
    ).all()

    return items



@router.get(
    "/restaurants/{restaurant_id}",
    response_model=RestaurantResponse
)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):

    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return restaurant
@router.get(
    "/restaurants",
    response_model=List[RestaurantResponse]
)
def get_all_restaurants(
    db: Session = Depends(get_db)
):

    restaurants = db.query(Restaurant).all()

    return restaurants
@router.get("/restaurant/orders")
def get_restaurant_orders(

    current_restaurant: Restaurant =
    Depends(get_current_restaurant),

    db: Session = Depends(get_db)
):

    orders = db.query(Order).filter(
        Order.restaurant_id ==
        current_restaurant.id
    ).all()

    result = []

    for order in orders:

        result.append({

            "order_id": order.id,

            "customer_name":
                order.customer.customer_name,

            "customer_phone":
                order.customer.contact_phone,

            "total_amount":
                order.total_amount,

            "status":
                order.status,

            "created_at":
                order.created_at
        })

    return result

@router.get("/restaurant/orders")
def get_restaurant_orders(
    db: Session = Depends(get_db)
):

    orders = db.query(Order).filter(
        Order.restaurant_id == 1
    ).all()

    return orders

@router.put("/restaurant/orders/{order_id}")
def update_restaurant_order_status(
    order_id: int,
    order_data: OrderStatusUpdate,
    db: Session = Depends(get_db)
):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.status = order_data.status

    db.commit()

    db.refresh(order)

    return {
        "message": "Order status updated",
        "status": order.status
    }
@router.get("/restaurant/dashboard")
def restaurant_dashboard(
    current_restaurant: Restaurant = Depends(
        get_current_restaurant
    ),
    db: Session = Depends(get_db)
):

    orders = db.query(Order).filter(
        Order.restaurant_id ==
        current_restaurant.id
    ).all()

    return {
        "total_orders": len(orders),
        "pending_orders":
            len([
                o for o in orders
                if o.status == "Pending"
            ])
    }