import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv(
    "COREBANK_DATABASE_URL",
    "postgresql+psycopg://corebank:corebank@localhost:5432/corebank",
)


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
