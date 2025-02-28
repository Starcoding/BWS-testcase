from fastapi import APIRouter, Depends

from src.models.UserModel import User
from src.schemas.TransactionSchema import BalanceUpdate
from src.schemas.UserSchema import UserCreate, UserResponse, UserUpdate
from src.services.TransactionService import TransactionService
from src.services.UserService import UserService
from src.utils import get_current_user, get_staff_user

UserRouter = APIRouter(prefix="/v1/users", tags=["user"])


@UserRouter.post(
    "/user/", response_model=UserResponse, summary="Регистрация нового пользователя"
)
async def create_user_endpoint(
    user_in: UserCreate,
    user_service: UserService = Depends(),
):
    return await user_service.register_user(user_in)


@UserRouter.get(
    "/users/",
    response_model=list[UserResponse],
    summary="Получение списка пользователей",
)
async def list_users_endpoint(
    is_verified: bool | None = None,
    username: str | None = None,
    current_user: object = Depends(get_staff_user),
    user_service: UserService = Depends(),
):
    return await user_service.list_users(is_verified, username)


@UserRouter.put(
    "/user/{user_id}",
    response_model=UserResponse,
    summary="Обновление данных пользователя",
)
async def update_user_endpoint(
    user_id: int,
    user_in: UserUpdate,
    user_service: UserService = Depends(),
    current_user: User = Depends(get_current_user),
):
    return await user_service.update_user_info(user_id, user_in, current_user)


@UserRouter.delete("/user/{user_id}", summary="Удаление пользователя")
async def delete_user_endpoint(
    user_id: int,
    user_service: UserService = Depends(),
    current_user: User = Depends(get_staff_user),
):
    return await user_service.remove_user(user_id)


@UserRouter.patch(
    "/user/{user_id}/verify",
    response_model=UserResponse,
    summary="Верификация пользователя",
)
async def verify_user_endpoint(
    user_id: int,
    user_service: UserService = Depends(),
    current_user: User = Depends(get_staff_user),
):
    return await user_service.change_verification_status(user_id)


@UserRouter.patch(
    "/user/{user_id}/balance",
    response_model=UserResponse,
    summary="Обновление баланса пользователя",
)
async def update_balance_endpoint(
    user_id: int,
    balance_update: BalanceUpdate,
    transaction_service: TransactionService = Depends(),
    current_user: User = Depends(get_staff_user),
):
    return await transaction_service.update_balance(user_id, balance_update)
