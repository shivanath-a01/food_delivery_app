from sqlalchemy import Column, Integer, String, Float

from app.database import Base


class Offer(Base):

    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)

    coupon_code = Column(String, unique=True)

    discount_amount = Column(Float)

    minimum_order_amount = Column(Float)

