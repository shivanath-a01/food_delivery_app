from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
    TIMESTAMP
)

from datetime import datetime
from sqlalchemy.orm import relationship

from app.database import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    customer_id = Column(
        Integer,
        ForeignKey("customer.id")
    )

    total_amount = Column(Float)

    status = Column(
        String,
        default="Pending"
    )

    created_at = Column(
        TIMESTAMP,
        default=datetime.utcnow
    )

    customer = relationship(
        "Customer",
        backref="orders"
    )

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurant.id"),
        nullable=True
    )

    restaurant = relationship(
        "Restaurant",
        backref="orders"
    )

    delivery_partner_id = Column(
        Integer,
        ForeignKey("delivery_partners.id"),
        nullable=True
    )