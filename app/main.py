from fastapi import FastAPI
from app.database import engine, Base
from app.models.restaurant import Restaurant
from app.routes.restaurant_route import router as restaurant_router
from app.models.item import FoodItem
from app.routes.item_route import router as item_router
from app.models.cart import Cart
from app.routes.cart_route import router as cart_router


from app.models.customer import Customer
from app.routes.customer_route import router as customer_router
from app.models.order import Order
from app.models.order_item import OrderItem
from app.routes.order_route import router as order_router
from app.models.payment import Payment
from app.routes.payment_route import router as payment_router
from app.models.review import Review
from app.routes.review_route import router as review_router
from app.models.offer import Offer
from app.routes.offer_route import router as offer_router
from app.models.delivery_partner import DeliveryPartner
from app.routes.delivery_partner_route import (
    router as delivery_partner_router
)
from app.routes.admin_route import (
    router as admin_router
)

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(restaurant_router)
app.include_router(item_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(review_router)
app.include_router(offer_router)
app.include_router(delivery_partner_router)
app.include_router(admin_router)

app.include_router(customer_router)

@app.get("/")
def home():
    return {"message": "Food Delivery Backend Running"}