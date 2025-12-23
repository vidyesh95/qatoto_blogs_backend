"""
This file mainly contains Pydantic schemas for models, used for validation and serialization.
"""

from typing import TypedDict

from pydantic import BaseModel


class BlogSchema(BaseModel):
    """Pydantic schema for Blog response - maps SQLAlchemy model fields."""

    id: int
    title: str
    description: str
    content: str

    class Config:
        from_attributes = True  # Allows creating from SQLAlchemy model instances


class BlogCreate(BaseModel):
    title: str
    description: str
    content: str


class Blogs(BaseModel):
    blog: BlogSchema


class BlogResponse(BaseModel):
    """Response schema for single blog with full content."""

    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


class BlogsResponse(BaseModel):
    """Response schema for blog list (without full content)."""

    id: int
    title: str
    description: str

    class Config:
        from_attributes = True


class BlogTable(TypedDict):
    blog_id: int
    title: str
    description: str
    content: str
