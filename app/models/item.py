from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    TIMESTAMP
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.database import Base

class FoodItem(Base):

    __tablename__ = "food_item"

    id = Column(Integer, primary_key=True, index=True)

    item_name = Column(String, nullable=False)

    description = Column(String)

    price = Column(Float, nullable=False)

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurant.id")
    )

    created_at = Column(
        TIMESTAMP,
        default=datetime.utcnow
    )

    restaurant = relationship(
        "Restaurant",
        backref="food_items"
    )
    