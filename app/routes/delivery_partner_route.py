from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.delivery_schema import (
    DeliveryStatusUpdate
)

from app.deps import get_db

from app.models.delivery_partner import (
    DeliveryPartner
)

from app.schemas.delivery_partner_schema import (
    DeliveryPartnerCreate
)


router = APIRouter()


@router.post("/delivery-partners")
def create_delivery_partner(
    partner_data: DeliveryPartnerCreate,
    db: Session = Depends(get_db)
):

    partner = DeliveryPartner(
        name=partner_data.name,
        phone=partner_data.phone,
        vehicle_number=partner_data.vehicle_number
    )

    db.add(partner)

    db.commit()

    db.refresh(partner)

    return {
        "message": "Delivery partner added"
    }

@router.post(
    "/delivery/assign/{order_id}/{partner_id}"
)
def assign_delivery_partner(
    order_id: int,
    partner_id: int,
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

    partner = db.query(
        DeliveryPartner
    ).filter(
        DeliveryPartner.id == partner_id
    ).first()

    if not partner:
        raise HTTPException(
            status_code=404,
            detail="Delivery partner not found"
        )

    if not partner.is_available:
        raise HTTPException(
            status_code=400,
            detail="Partner not available"
        )

    order.delivery_partner_id = partner.id

    partner.is_available = False

    db.commit()

    return {
        "message": "Delivery partner assigned",
        "partner": partner.name
    }
@router.put("/delivery/status/{order_id}")
def update_delivery_status(
    order_id: int,
    delivery_data: DeliveryStatusUpdate,
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

    order.status = delivery_data.status

    if delivery_data.status == "Delivered":

        partner = db.query(
            DeliveryPartner
        ).filter(
            DeliveryPartner.id ==
            order.delivery_partner_id
        ).first()

        if partner:
            partner.is_available = True

    db.commit()

    return {
        "message": "Delivery status updated",
        "new_status": order.status
    }
@router.get("/delivery/{order_id}")
def get_delivery_details(
    order_id: int,
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

    if not order.delivery_partner_id:
        raise HTTPException(
            status_code=404,
            detail="Delivery partner not assigned"
        )

    partner = db.query(
        DeliveryPartner
    ).filter(
        DeliveryPartner.id ==
        order.delivery_partner_id
    ).first()

    return {
        "order_id": order.id,
        "delivery_partner": partner.name,
        "phone": partner.phone,
        "vehicle_number": partner.vehicle_number,
        "status": order.status
    }
