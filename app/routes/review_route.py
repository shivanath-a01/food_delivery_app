from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from typing import List

from app.auth.token import get_current_user

from app.models.customer import Customer
from app.models.review import Review

from app.schemas.review_schema import (
    ReviewCreate,
    ReviewResponse
)



router = APIRouter()


@router.post("/reviews/{restaurant_id}")
def add_review(
    restaurant_id: int,
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user)
):

    review = Review(
        customer_id=current_user.id,
        restaurant_id=restaurant_id,
        rating=review_data.rating,
        comment=review_data.comment
    )

    db.add(review)

    db.commit()

    return {
        "message": "Review added successfully"
    }
@router.get(
    "/reviews/{restaurant_id}",
    response_model=List[ReviewResponse]
)
def get_reviews(
    restaurant_id: int,
    db: Session = Depends(get_db)
):

    reviews = db.query(Review).filter(
        Review.restaurant_id == restaurant_id
    ).all()

    return reviews
