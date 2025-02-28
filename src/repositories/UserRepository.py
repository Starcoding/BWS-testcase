from fastapi import Depends
from sqlalchemy.orm import Session

from src.db import get_db
from src.models.UserModel import User


class UserRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    async def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    async def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    async def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    async def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    async def update_user(self, user: User, update_data: dict) -> User:
        for key, value in update_data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    async def delete_user(self, user: User):
        self.db.delete(user)
        self.db.commit()

    async def list_users(
        self, is_verified: bool | None = None, username: str | None = None
    ) -> list[User]:
        query = self.db.query(User)
        if is_verified is not None:
            query = query.filter(User.is_verified == is_verified)
        if username:
            query = query.filter(User.username.contains(username))
        return query.all()

    async def change_verification_status(
        self, user_id: int, new_status: bool = True
    ) -> User | None:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        user.is_verified = new_status  # type: ignore
        self.db.commit()
        self.db.refresh(user)
        return user
