from fastapi import APIRouter, Depends, Query

from sqlalchemy.orm import Session
from app.models.item import FoodItem


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


