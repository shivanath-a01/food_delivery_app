from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.database import Base


class Review(Base):

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)

    customer_id = Column(
        Integer,
        ForeignKey("customer.id")
    )

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurant.id")
    )

    rating = Column(Integer)

    comment = Column(String)
    