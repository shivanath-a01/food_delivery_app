from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.schemas.cart_schema import CartCreate
from app.deps import get_db
from typing import List
from app.schemas.cart_schema import (
    CartCreate,
    CartItemResponse,
    CartResponse,
    CartQuantityUpdate
)




from app.auth.token import get_current_user
from app.models.customer import Customer

router = APIRouter()

@router.post("/cart/add")
def add_to_cart(
    cart: CartCreate,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user)
):

    new_cart_item = Cart(
        customer_id=current_user.id,
        food_item_id=cart.food_item_id,
        quantity=cart.quantity
    )

    db.add(new_cart_item)

    db.commit()

    db.refresh(new_cart_item)

    return {
        "message": "Item added to cart"
    }
@router.get(
    "/cart",
    response_model=CartResponse
)
def get_cart(
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user)
):

    cart_items = db.query(Cart).filter(
        Cart.customer_id == current_user.id
    ).all()

    response_items = []

    grand_total = 0

    for cart_item in cart_items:

        unit_price = cart_item.food_item.price

        total_price = unit_price * cart_item.quantity

        grand_total += total_price

        response_items.append({
            "id": cart_item.id,
            "quantity": cart_item.quantity,
            "unit_price": unit_price,
            "total_price": total_price,
            "food_item": cart_item.food_item
        })

    return {
        "cart_items": response_items,
        "grand_total": grand_total
    }

@router.delete("/cart/{cart_id}")
def remove_cart_item(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user)
):

    cart_item = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.customer_id == current_user.id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    db.delete(cart_item)

    db.commit()

    return {
        "message": "Cart item removed successfully"
    }

@router.put("/cart/{cart_id}")
def update_cart_quantity(
    cart_id: int,
    cart_data: CartQuantityUpdate,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user)
):

    cart_item = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.customer_id == current_user.id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    cart_item.quantity = cart_data.quantity

    db.commit()

    db.refresh(cart_item)

    return {
        "message": "Cart quantity updated",
        "new_quantity": cart_item.quantity
    }

