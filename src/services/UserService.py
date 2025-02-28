from fastapi import Depends, HTTPException

from src.models.UserModel import User
from src.repositories.TransactionRepository import TransactionRepository
from src.repositories.UserRepository import UserRepository
from src.schemas.UserSchema import UserCreate, UserUpdate
from src.utils import generate_password, hash_password


class UserService:
    user_repository: UserRepository
    transaction_repository: TransactionRepository

    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        transaction_repository: TransactionRepository = Depends(),
    ):
        self.user_repository = user_repository
        self.transaction_repository = transaction_repository

    async def register_user(self, user_in: UserCreate) -> User:
        if await self.user_repository.get_user_by_username(user_in.username):
            raise HTTPException(status_code=400, detail="Username уже существует")
        if await self.user_repository.get_user_by_email(user_in.email):
            raise HTTPException(status_code=400, detail="Email уже существует")

        raw_password = user_in.password or generate_password()
        hashed_password = hash_password(raw_password)

        user = User(
            username=user_in.username,
            email=user_in.email,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            city=user_in.city,
            country=user_in.country,
            password=hashed_password,
        )
        return await self.user_repository.create_user(user)

    async def update_user_info(
        self, user_id: int, user_in: UserUpdate, current_user: User
    ) -> User:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        if not current_user.is_staff and current_user.id != user.id:
            raise HTTPException(
                status_code=403, detail="Нет прав для редактирования этого пользователя"
            )

        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])
        return await self.user_repository.update_user(user, update_data)

    async def remove_user(self, user_id: int):
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        await self.user_repository.delete_user(user)
        return {"detail": "Пользователь удален"}

    async def list_users(
        self, is_verified: bool | None, username: str | None
    ) -> list[User]:
        return await self.user_repository.list_users(is_verified, username)

    async def change_verification_status(self, user_id: int) -> User:
        user = await self.user_repository.change_verification_status(user_id, True)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user
