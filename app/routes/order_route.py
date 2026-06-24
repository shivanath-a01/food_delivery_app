from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db

from app.auth.token import get_current_user
from typing import List
from app.schemas.order_schema import (
    OrderResponse,
    OrderItemResponse,
    OrderStatusUpdate
)


from app.models.customer import Customer
from app.models.cart import Cart
from app.models.order import Order
from app.models.order_item import OrderItem

router = APIRouter()

@router.post("/orders/place")
def place_order(
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user)
):

    cart_items = db.query(Cart).filter(
        Cart.customer_id == current_user.id
    ).all()

    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    grand_total = 0

    for cart_item in cart_items:

        total_price = (
            cart_item.quantity *
            cart_item.food_item.price
        )

        grand_total += total_price

    new_order = Order(
    customer_id=current_user.id,
    restaurant_id=cart_items[0].food_item.restaurant_id,
    total_amount=grand_total
    )
    db.add(new_order)

    db.commit()

    db.refresh(new_order)

    for cart_item in cart_items:

        unit_price = cart_item.food_item.price

        total_price = (
            unit_price *
            cart_item.quantity
        )

        order_item = OrderItem(
            order_id=new_order.id,
            food_item_id=cart_item.food_item_id,
            quantity=cart_item.quantity,
            item_price=unit_price,
            total_price=total_price
        )

        db.add(order_item)

    db.commit()

    for cart_item in cart_items:
        db.delete(cart_item)

    db.commit()

    return {
        "message": "Order placed successfully",
        "order_id": new_order.id,
        "total_amount": grand_total
    }

@router.get(
    "/orders",
    response_model=List[OrderResponse]
)
def get_orders(
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user)
):

    orders = db.query(Order).filter(
        Order.customer_id == current_user.id
    ).all()

    response = []

    for order in orders:

        order_items = []

        for item in order.order_items:

            order_items.append({
                "food_item_name": item.food_item.item_name,
                "quantity": item.quantity,
                "item_price": item.item_price,
                "total_price": item.total_price
            })

        response.append({
            "order_id": order.id,
            "total_amount": order.total_amount,
            "status": order.status,
            "items": order_items
        })

    return response
@router.put("/orders/status/{order_id}")
def update_order_status(
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
        "new_status": order.status
    }

