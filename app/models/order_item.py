from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database import Base

class OrderItem(Base):

    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id")
    )

    food_item_id = Column(
        Integer,
        ForeignKey("food_item.id")
    )

    quantity = Column(Integer)

    item_price = Column(Float)

    total_price = Column(Float)

    order = relationship(
        "Order",
        backref="order_items"
    )

    food_item = relationship(
        "FoodItem"
    )
    