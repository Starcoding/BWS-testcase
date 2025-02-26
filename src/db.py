from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.settings import settings

if settings.DEBUG:
    engine = create_engine(settings.database_url, echo=True)
else:
    engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
