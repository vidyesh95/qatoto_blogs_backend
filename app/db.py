"""
This file contains the database connection and functions
"""
from typing import Any, AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # noqa: ERA001


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models

    All models should inherit from this class.
    """
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


async_engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)

async def get_async_db_session() -> AsyncGenerator[AsyncSession, Any]:
    """
    Get an async database session

    To be used for dependency injection
    """
    async with async_session() as session, session.begin():
        yield session


async def init_models() -> None:
    """
    Create tables in the database if they don't exist

    In a real-life example we would use Alembic to manage database migrations
    """
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # noqa: ERA001
        await conn.run_sync(Base.metadata.create_all)

