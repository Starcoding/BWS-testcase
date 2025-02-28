from decimal import Decimal

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    city: str | None = None
    country: str | None = None
    password: str | None = None


class UserUpdate(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    city: str | None = None
    country: str | None = None
    password: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    city: str | None = None
    country: str | None = None
    balance: Decimal = Field(..., max_digits=10, decimal_places=2)
    is_verified: bool
    is_staff: bool

    class Config:
        from_attributes = True
