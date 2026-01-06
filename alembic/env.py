"""
Alembic environment configuration for async SQLAlchemy.

This module configures Alembic to work with asyncpg driver and
automatically detects model changes for migration autogeneration.
"""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Import your Base and DATABASE_URL from the app
from app.db import DATABASE_URL, Base

# Import all models here so that Base.metadata is populated
# This is required for autogenerate to detect your models
from app import models  # noqa: F401

# =============================================================================
# Alembic Configuration
# =============================================================================
config = context.config

# Dynamically set the database URL from your app config
# This overrides the placeholder in alembic.ini
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Set up Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Point Alembic to your models' metadata for autogenerate support
# This allows Alembic to detect changes in your models automatically
target_metadata = Base.metadata


# =============================================================================
# Offline Migration Mode
# =============================================================================
def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This generates SQL scripts without connecting to the database.
    Useful for generating migration scripts for review or manual execution.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# =============================================================================
# Online Migration Mode (Async)
# =============================================================================
def do_run_migrations(connection) -> None:
    """
    Execute migrations using the provided database connection.

    This is a synchronous helper function that is called within
    the async context using connection.run_sync().
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # Compare types for more accurate autogenerate results
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode using async engine.

    Creates an async database connection and runs migrations.
    This is the mode used when you run `alembic upgrade head`.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # run_sync allows us to run synchronous migration code
        # within the async connection context
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# =============================================================================
# Entry Point
# =============================================================================
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
