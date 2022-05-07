from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
import os

SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_URL")

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,  # connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(expire_on_commit=True, bind=engine, class_=AsyncSession)

Base = declarative_base()
