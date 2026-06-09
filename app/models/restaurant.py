from sqlalchemy import Column, Integer, String, TIMESTAMP
from datetime import datetime
from app.database import Base

class Restaurant(Base):

    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True, index=True)

    restaurant_name = Column(String, nullable=False)

    restaurant_address = Column(String)

    contact_phone = Column(String)

    email = Column(
        String,
        unique=True,
        nullable=True
    )

    password = Column(
        String,
        nullable=True
    )

    created_at = Column(
        TIMESTAMP,
        default=datetime.utcnow
    )
    