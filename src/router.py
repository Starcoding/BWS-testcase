from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db import get_db
from src.models import Transaction, User
from src.schemas import BalanceUpdate, UserCreate, UserResponse, UserUpdate
from src.service import (generate_password, get_current_user, get_staff_user,
                         hash_password)

router = APIRouter()


@router.post(
    "/user/",
    response_model=UserResponse,
)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Username уже существует")
    if db.query(User).filter(User.email == user_in.email).first():
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
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("/users/", response_model=list[UserResponse])
def list_users(
    is_verified: bool | None = None,
    username: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_staff_user),
):
    query = db.query(User)
    if is_verified is not None:
        query = query.filter(User.is_verified == is_verified)
    if username:
        query = query.filter(User.username.contains(username))
    return query.all()


@router.put("/user/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if not current_user.is_staff and current_user.id != user.id:
        raise HTTPException(
            status_code=403, detail="Нет прав для редактирования этого пользователя"
        )

    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/user/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_staff_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(user)
    db.commit()
    return {"detail": "Пользователь удален"}


@router.patch("/user/{user_id}/verify", response_model=UserResponse)
def change_verification_status(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_staff_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user.is_verified = True  # type: ignore
    db.commit()
    db.refresh(user)
    return user


@router.patch("/user/{user_id}/balance", response_model=UserResponse)
def update_balance(
    user_id: int,
    balance_update: BalanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_staff_user),
):
    user = db.query(User).filter(User.id == user_id).with_for_update().first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Пользователь не верифицирован")

    existing_tx = (
        db.query(Transaction)
        .filter(
            Transaction.user_id == user_id,
            Transaction.transaction_id == balance_update.transaction_id,
        )
        .first()
    )
    if existing_tx:
        raise HTTPException(status_code=400, detail="Транзакция уже была обработана")

    user.balance += balance_update.amount  # type: ignore

    transaction = Transaction(
        user_id=user_id,
        transaction_id=balance_update.transaction_id,
        amount=balance_update.amount,
    )
    db.add(transaction)

    db.commit()
    db.refresh(user)
    return user
