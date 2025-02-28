from decimal import Decimal

from pydantic import BaseModel, Field


class BalanceUpdate(BaseModel):
    amount: Decimal = Field(..., max_digits=10, decimal_places=2)
    transaction_id: str
