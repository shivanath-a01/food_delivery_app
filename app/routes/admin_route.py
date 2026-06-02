from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.auth.token import get_current_admin
from app.models.customer import Customer

from app.deps import get_db
from app.models.order_item import OrderItem

from app.models.customer import Customer
from app.models.restaurant import Restaurant
from app.models.order import Order


router = APIRouter()


@router.get("/admin/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    current_admin: Customer = Depends(get_current_admin)
):

    total_customers = db.query(
        Customer
    ).count()

    total_restaurants = db.query(
        Restaurant
    ).count()

    total_orders = db.query(
        Order
    ).count()

    total_revenue = db.query(
        func.sum(Order.total_amount)
    ).scalar()

    return {
        "total_customers": total_customers,
        "total_restaurants": total_restaurants,
        "total_orders": total_orders,
        "total_revenue": total_revenue
    }

@router.get("/admin/top-items")
def top_selling_items(
    db: Session = Depends(get_db),
    current_admin: Customer = Depends(get_current_admin)
):

    items = db.query(
        OrderItem.food_item_id,
        func.sum(OrderItem.quantity).label(
            "total_quantity"
        )
    ).group_by(
        OrderItem.food_item_id
    ).all()

    return items
