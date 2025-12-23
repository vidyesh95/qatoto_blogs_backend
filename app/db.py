"""
This file contains the database connection and functions
"""
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/postgres"
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # noqa: ERA001

async_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})