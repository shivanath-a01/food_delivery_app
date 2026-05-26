from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db

from app.models.payment import Payment
from app.models.order import Order

from app.schemas.payment_schema import PaymentCreate


router = APIRouter()


@router.post("/payments/pay/{order_id}")
def make_payment(
    order_id: int,
    payment_data: PaymentCreate,
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

    payment = Payment(
        order_id=order.id,
        payment_method=payment_data.payment_method,
        payment_status="Paid"
    )

    db.add(payment)

    order.status = "Paid"

    db.commit()

    db.refresh(payment)

    return {
        "message": "Payment successful",
        "payment_status": payment.payment_status
    }
