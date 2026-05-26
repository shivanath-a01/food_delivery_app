from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db

from app.models.offer import Offer
from app.models.order import Order

from app.schemas.offer_schema import OfferApply


router = APIRouter()


@router.post("/offers/apply/{order_id}")
def apply_offer(
    order_id: int,
    offer_data: OfferApply,
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

    offer = db.query(Offer).filter(
        Offer.coupon_code == offer_data.coupon_code
    ).first()

    if not offer:
        raise HTTPException(
            status_code=404,
            detail="Invalid coupon code"
        )

    if order.total_amount < offer.minimum_order_amount:
        raise HTTPException(
            status_code=400,
            detail="Order amount too low for this coupon"
        )

    final_amount = (
        order.total_amount -
        offer.discount_amount
    )

    return {
        "original_amount": order.total_amount,
        "discount": offer.discount_amount,
        "final_amount": final_amount
    }
