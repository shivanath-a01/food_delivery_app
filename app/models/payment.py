from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Payment(Base):

    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id")
    )

    payment_method = Column(String)

    payment_status = Column(String)
    