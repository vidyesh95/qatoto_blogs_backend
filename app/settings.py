"""
Application settings and environment configuration.

This module provides:
- Environment variable loading from .env files
- Safe environment variable access with validation
- Database connection string construction
- Configuration constants used throughout the application
"""

import os

from dotenv import load_dotenv

# =============================================================================
# Environment Variable Loading
# =============================================================================
# Load environment variables from .env file if it exists.
# This should be called early in the application startup to ensure
# all subsequent os.environ lookups can access the .env values.
#
# Note: If a variable is already set in the system environment,
# it will NOT be overwritten by the .env file value.
load_dotenv()


# =============================================================================
# Sentinel Value for Missing Arguments
# =============================================================================
# This sentinel pattern allows us to distinguish between:
# 1. A caller not providing a default value at all
# 2. A caller explicitly providing None or an empty string as default
#
# Without this pattern, we couldn't tell the difference between:
#   get_env_var("KEY")           -> should raise error if KEY is missing
#   get_env_var("KEY", None)     -> should return None if KEY is missing
#
# Both would result in default=None, making them indistinguishable.


class _NoArg:
    """
    A sentinel class to indicate that a parameter was not provided.

    This is used internally by get_env_var() to distinguish between
    "no default given" and "default is None or empty string".
    """


NO_ARG = _NoArg()


# =============================================================================
# Environment Variable Helper
# =============================================================================
def get_env_var(key: str, default: str | _NoArg = NO_ARG) -> str:
    """
    Safely retrieve an environment variable with optional default.

    This function provides a consistent way to access environment variables
    with proper error handling. If a variable is missing and no default
    is provided, it raises a descriptive error message.

    Args:
        key: The name of the environment variable to retrieve.
        default: Optional fallback value if the variable is not set.
                 If not provided and the variable is missing, raises ValueError.

    Returns:
        The value of the environment variable, or the default if provided.

    Raises:
        ValueError: If the environment variable is missing and no default
                    was provided.

    Examples:
        # Required variable - raises error if missing
        secret_key = get_env_var("SECRET_KEY")

        # Optional variable with fallback
        debug_mode = get_env_var("DEBUG", "false")
    """
    try:
        return os.environ[key]
    except KeyError:
        if isinstance(default, _NoArg):
            raise ValueError(f"Environment variable {key} is missing")

        return default


# =============================================================================
# Database Configuration
# =============================================================================
# These environment variables are used to construct the database URL.
# All are required - the application will fail to start if any are missing.
#
# Required environment variables in .env:
#   PG_HOST     - PostgreSQL server hostname (e.g., "localhost")
#   PG_PORT     - PostgreSQL server port (e.g., "5432")
#   PG_USER     - Database username (e.g., "postgres")
#   PG_PASSWORD - Database password
#   PG_DB       - Database name (e.g., "myapp")
PG_HOST = get_env_var("PG_HOST")
PG_PORT = get_env_var("PG_PORT")
PG_USER = get_env_var("PG_USER")
PG_PASSWORD = get_env_var("PG_PASSWORD")
PG_DB = get_env_var("PG_DB")

# Construct the full database URL for SQLAlchemy.
# Format: postgresql+asyncpg://user:password@host:port/database
#
# We use the asyncpg driver for async database operations with SQLAlchemy.
# This URL is imported by db.py to create the database engine.
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
)

# =============================================================================
# SQLAlchemy Configuration
# =============================================================================
# SQLALCHEMY_ECHO controls whether SQL statements are logged to the console.
# Set to "true" in .env for debugging, remove or set to anything else for production.
#
# Note: This is a string comparison because environment variables are always strings.
SQLALCHEMY_ECHO = get_env_var("SQLALCHEMY_ECHO", "") == "true"
