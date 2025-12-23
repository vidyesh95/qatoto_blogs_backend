"""
Set up the database connection and session.

This module provides:
- Database connection configuration
- Base class for SQLAlchemy models with consistent naming conventions
- Async database engine and session management
- Dependency injection helper for database sessions
- Table initialization utility
"""

from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# =============================================================================
# Database Connection String
# =============================================================================
# We set a variable containing the database URL. We are using PostgreSQL with
# asyncpg driver for async support. You can use any database that SQLAlchemy
# supports.
#
# Format: postgresql+asyncpg://user:password@host:port/database
#
# Note: In production, you should use environment variables to store
# sensitive credentials like user/password and database name.
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # SQLite alternative for testing  # noqa: ERA001


# =============================================================================
# Base Class for SQLAlchemy Models
# =============================================================================
class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models.

    All other models should inherit from this class. This class extends
    DeclarativeBase and adds a metadata attribute with a consistent naming
    convention for database constraints.

    The naming convention ensures:
    - ix_<column>: Index names
    - uq_<table>_<column>: Unique constraint names
    - ck_<table>_<constraint>: Check constraint names
    - fk_<table>_<column>_<referred_table>: Foreign key names
    - pk_<table>: Primary key names

    Note: The naming convention is not required, but it's a good practice
    for consistency and makes database migrations easier to manage.
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


# =============================================================================
# Database Engine and Session
# =============================================================================
# Create the async database engine.
# The create_async_engine function takes the database URL and returns an engine,
# which is the connection to the database.
#
# Parameters:
# - DATABASE_URL: The connection string for the database
# - echo: Set to True to log all SQL commands (useful for debugging),
#         set to False in production to reduce noise
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Create the async session factory.
# The async_sessionmaker function takes the engine and returns a session factory.
#
# Parameters:
# - async_engine: The database engine to bind sessions to
# - expire_on_commit: Set to False to prevent SQLAlchemy from expiring objects
#                     on commit. This is required for asyncpg to work properly.
#
# Note: We do NOT use this session directly. Instead, use the
# get_async_db_session() function below for dependency injection.
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


# =============================================================================
# Database Session Dependency
# =============================================================================
async def get_async_db_session() -> AsyncGenerator[AsyncSession, Any]:
    """
    Get a database session as an async generator.

    This function is used for dependency injection in FastAPI routes.
    It provides a database session that is automatically closed (and data
    committed) when the function returns, usually after the related route
    is complete.

    Usage in FastAPI:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_async_db_session)):
            # use db session here
            pass

    Note: We use a combined 'with' statement as a shortcut for two nested
    'with' statements - one for async_session() and one for session.begin().
    This ensures:
    1. The session is properly acquired and released
    2. A transaction is started and committed/rolled back automatically

    Yields:
        AsyncSession: An active database session within a transaction
    """
    async with async_session() as session, session.begin():
        yield session


# =============================================================================
# Table Initialization
# =============================================================================
async def init_models() -> None:
    """
    Create database tables if they don't already exist.

    This function demonstrates how to run a synchronous function in an async
    context using the async_engine object directly. The run_sync() method
    is used to execute Base.metadata.create_all() which is a synchronous
    operation.

    Warning: This function is only for demo/development purposes!
    In a real-life production application, you should use a migration tool
    like Alembic (https://alembic.sqlalchemy.org/) to manage database schema
    changes and migrations.

    To drop and recreate tables on every server restart (useful for testing),
    uncomment the drop_all line below. Obviously, DO NOT use this in production
    as it will delete all your data!
    """
    async with async_engine.begin() as conn:
        # Uncomment below to drop all tables before recreating (DANGEROUS!)
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
