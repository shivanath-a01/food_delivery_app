from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean
)

from app.database import Base


class DeliveryPartner(Base):

    __tablename__ = "delivery_partners"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    email = Column(String, unique=True)

    password = Column(String)

    phone = Column(String)

    vehicle_type = Column(String)

    vehicle_number = Column(String)

    license_number = Column(String)

    is_available = Column(
        Boolean,
        default=True
    )
    