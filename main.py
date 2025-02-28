from fastapi import FastAPI

from src.db import init_db
from src.routers.v1.UserRouter import UserRouter
from src.settings import settings
from src.utils import create_staff_user

app = FastAPI()

init_db()

app.include_router(UserRouter)

if settings.DEBUG:
    create_staff_user()
