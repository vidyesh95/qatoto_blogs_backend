"""
Database Models for the Blog Application.

This module defines SQLAlchemy ORM models that represent database tables.
Each model class maps to a database table, and each instance of a model
represents a row in that table.

Models use SQLAlchemy 2.0 style with:
- Type-annotated columns using Mapped[] for better IDE support
- mapped_column() for column definitions
- Inheritance from Base (defined in db.py) for consistent table configuration
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


# =============================================================================
# Blog Model
# =============================================================================
class Blog(Base):
    """
    Blog post model representing the 'blogs' table in the database.

    This model stores blog articles with their metadata and content.
    Each blog post has a unique ID, title, description, and full content.

    Attributes:
        id: Primary key, auto-incremented integer. Indexed for fast lookups.
        title: Blog post title, max 100 characters. Indexed for search queries.
        description: Short summary/excerpt of the blog, max 500 characters.
        content: Full blog post content, stored as TEXT (unlimited length).

    Table Name:
        'blogs' (plural) - follows REST API naming conventions where
        the table contains multiple blog records.

    Example:
        >>> blog = Blog(
        ...     title="Getting Started with FastAPI",
        ...     description="A beginner's guide to building APIs",
        ...     content="Full article content here..."
        ... )
        >>> print(blog)
        Blog(id=None, title='Getting Started with FastAPI')
    """

    # Table name in the database (plural form for REST convention)
    __tablename__ = "blogs"

    # ==========================================================================
    # Column Definitions
    # ==========================================================================

    # Primary Key: Auto-incremented unique identifier
    # - primary_key=True: Makes this the primary key
    # - index=True: Creates a database index for faster lookups by ID
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Title: Short blog post title
    # - String(100): VARCHAR(100), limits title to 100 characters
    # - index=True: Creates index for faster title-based searches
    title: Mapped[str] = mapped_column(String(100), index=True)

    # Description: Brief summary or excerpt of the blog post
    # - String(500): VARCHAR(500), suitable for a short paragraph
    # - No index: Descriptions are typically not searched directly
    description: Mapped[str] = mapped_column(String(500))

    # Content: Full blog post body
    # - No String() type: Maps to TEXT in PostgreSQL (unlimited length)
    # - Suitable for long-form article content
    content: Mapped[str] = mapped_column()

    # ==========================================================================
    # Magic Methods
    # ==========================================================================

    def __repr__(self) -> str:
        """
        Return a developer-friendly string representation of the Blog instance.

        This method is called when:
        - Printing the object: print(blog)
        - Using repr(): repr(blog)
        - Debugging in IDE or console
        - Logging objects

        Only includes id and title (not description/content) to keep output
        readable and avoid flooding logs with large text blocks.

        The !r format specifier adds quotes around string values, making it
        clear that title is a string: title='Hello' instead of title=Hello

        Returns:
            str: String representation like "Blog(id=1, title='My Post')"
        """
        return f"Blog(id={self.id!r}, title={self.title!r})"
