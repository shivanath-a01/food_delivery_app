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

    phone = Column(String)

    vehicle_number = Column(String)

    is_available = Column(
        Boolean,
        default=True
    )

