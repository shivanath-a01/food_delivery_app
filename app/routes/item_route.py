from fastapi import APIRouter, Depends, HTTPException, Query



from sqlalchemy.orm import Session

from app.models.item import FoodItem
from app.schemas.item_schema import (
    FoodItemCreate,
    FoodItemResponse
)

from app.deps import get_db
from typing import List


router = APIRouter()

@router.post("/items")
def create_food_item(
    item: FoodItemCreate,
    db: Session = Depends(get_db)
):

    new_item = FoodItem(
        item_name=item.item_name,
        description=item.description,
        price=item.price,
        restaurant_id=item.restaurant_id
    )

    db.add(new_item)

    db.commit()

    db.refresh(new_item)

    return {
        "message": "Food item created successfully"
    }
@router.get(
    "/items",
    response_model=List[FoodItemResponse]
)
def get_all_items(
    db: Session = Depends(get_db)
):

    items = db.query(FoodItem).all()

    return items

@router.get(
    "/items/search",
    response_model=List[FoodItemResponse]
)
def search_food_items(
    keyword: str = Query(...),
    db: Session = Depends(get_db)
):

    items = db.query(FoodItem).filter(
        FoodItem.item_name.ilike(f"%{keyword}%")
    ).all()

    return items


@router.get(
    "/items/{item_id}",
    response_model=FoodItemResponse
)
def get_single_item(
    item_id: int,
    db: Session = Depends(get_db)
):

    item = db.query(FoodItem).filter(
        FoodItem.id == item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Food item not found"
        )

    return item

