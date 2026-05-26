from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    TIMESTAMP
)

from datetime import datetime

from sqlalchemy.orm import relationship

from app.database import Base

class Cart(Base):

    __tablename__ = "cart"

    id = Column(Integer, primary_key=True)

    customer_id = Column(
        Integer,
        ForeignKey("customer.id")
    )

    food_item_id = Column(
        Integer,
        ForeignKey("food_item.id")
    )

    quantity = Column(Integer, default=1)

    created_at = Column(
        TIMESTAMP,
        default=datetime.utcnow
    )

    customer = relationship(
        "Customer",
        backref="cart_items"
    )

    food_item = relationship(
        "FoodItem",
        backref="cart_items"
    )

