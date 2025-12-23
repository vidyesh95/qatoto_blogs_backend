"""
This file contains the database models
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

class Blog(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(String(500))
    content: Mapped[str] = mapped_column()

    def __repr__(self):
        """
        Define the model representation
        """
        return f"Blog(id={self.id!r}, title={self.title!r})"
