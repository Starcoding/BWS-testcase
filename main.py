from fastapi import FastAPI

from src.db import init_db
from src.router import router
from src.service import create_staff_user
from src.settings import settings

app = FastAPI()

init_db()

app.include_router(router)

if settings.DEBUG:
    create_staff_user()
