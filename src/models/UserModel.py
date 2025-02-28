from sqlalchemy import Boolean, Column, Integer, Numeric, String

from src.models.BaseModel import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    balance = Column(Numeric(precision=10, scale=2), default=0, server_default="0")
    is_verified = Column(Boolean, default=False, server_default="false")
    is_staff = Column(Boolean, default=False, server_default="false")
    password = Column(String, nullable=False)
