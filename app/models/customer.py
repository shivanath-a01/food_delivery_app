from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from app.database import Base
from datetime import datetime

class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String, nullable=False)

    contact_phone = Column(String, unique=True)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    confirmation_code = Column(String)

    time_joined = Column(TIMESTAMP, default=datetime.utcnow)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    created_by = Column(String)

    modified_at = Column(TIMESTAMP)

    modified_by = Column(String)

    is_deleted = Column(Boolean, default=False)