import random
import string
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.db import SessionLocal, get_db
from src.models import User
from src.settings import settings

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
) -> Optional[User] | None:
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, str(user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


def get_staff_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ только для staff пользователей",
        )
    return current_user


def generate_password(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def create_staff_user():
    db = SessionLocal()
    try:
        if settings.DEBUG:
            admin = db.query(User).filter(User.username == "admin").first()
            if not admin:
                admin = User(
                    username="admin",
                    email="admin@example.com",
                    first_name="Admin",
                    last_name="User",
                    is_staff=True,
                    is_verified=True,
                    password=hash_password(settings.BASIC_AUTH_PASSWORD),
                )
                db.add(admin)
                db.commit()
                print("Создан staff-пользователь: admin")
    finally:
        db.close()
