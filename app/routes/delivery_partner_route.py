from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
from app.auth.token import (
    create_access_token
)
from app.schemas.delivery_partner_schema import (
    DeliveryPartnerCreate,
    DeliveryPartnerLogin
)

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

    existing_partner = db.query(
        DeliveryPartner
    ).filter(
        DeliveryPartner.email ==
        partner_data.email
    ).first()

    if existing_partner:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(
        partner_data.password
    )

    partner = DeliveryPartner(
        name=partner_data.name,
        email=partner_data.email,
        password=hashed_password,
        phone=partner_data.phone,
        vehicle_type=partner_data.vehicle_type,
        vehicle_number=partner_data.vehicle_number,
        license_number=partner_data.license_number
    )

    db.add(partner)

    db.commit()

    db.refresh(partner)

    return {
        "message": "Delivery partner created successfully"
    }


@router.post("/delivery/login")
def delivery_login(
    login_data: DeliveryPartnerLogin,
    db: Session = Depends(get_db)
):

    partner = db.query(
        DeliveryPartner
    ).filter(
        DeliveryPartner.email ==
        login_data.email
    ).first()

    if not partner:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not pwd_context.verify(
        login_data.password,
        partner.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": partner.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "partner_name": partner.name
    }

@router.get("/delivery/orders/available")
def get_available_orders(
    db: Session = Depends(get_db)
):

    orders = db.query(Order).filter(
        Order.status == "Pending",
        Order.delivery_partner_id == None
    ).all()

    return orders

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
