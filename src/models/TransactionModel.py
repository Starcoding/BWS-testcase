from sqlalchemy import Column, ForeignKey, Integer, Numeric, String

from src.models.BaseModel import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    transaction_id = Column(String, unique=True, nullable=False, index=True)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
