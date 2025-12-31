"""
This file mainly contains routes.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from enum import Enum
from typing import Annotated, Any, Sequence

from fastapi import FastAPI, HTTPException, status
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_db_session, init_models
from app.models import Blog
from app.schemas import BlogCreate, BlogSchema, BlogResponse, BlogsResponse

PROJECT_DESCRIPTION = """
Qatoto Blogs API

Qatoto Blogs is a simple API for managing blogs.
"""


@asynccontextmanager
async def lifespan(_fastapi_app: FastAPI) -> AsyncGenerator[Any, None]:
    """Run tasks before and after the server starts"""
    await init_models()
    yield


app = FastAPI(
    title="Qatoto Blogs",
    description=PROJECT_DESCRIPTION,
    summary="Qatoto Blogs API",
    version="0.0.1",
    lifespan=lifespan,
)


class Tags(Enum):
    """API tags for grouping documentation"""

    BLOGS = "blogs"
    AUTH = "auth"


# =============================================================================
# READ Operations
# =============================================================================


@app.get(
    "/",
    response_model=list[BlogsResponse],
    tags=[Tags.BLOGS],
    summary="Read all blogs",
    description="Read all blogs",
    response_description="List of all blogs",
)
async def get_blogs(
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> Sequence[Blog]:
    """
    Read all blogs

    Returns:
        list[BlogsResponse]: List of all blogs
    """
    result = await session.execute(select(Blog))
    blogs = result.scalars().all()
    if not blogs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No blogs found",
        )
    return blogs


@app.get(
    "/blog/{blog_id}",
    response_model=BlogResponse,
    tags=[Tags.BLOGS],
    summary="Read a blog",
    description="Read a blog by id",
    response_description="The blog with the given id",
)
async def get_blog(
    blog_id: Annotated[int, "Enter the blog id to read the blog"],
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> Blog:
    """
    Read a blog by id

    Args:
        blog_id (int): The id of the blog to read

    Returns:
        Blog: The blog with the given id
    """
    result = await session.execute(select(Blog).where(Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found",
        )
    return blog


# =============================================================================
# CREATE Operations
# =============================================================================


@app.post(
    "/create-blog",
    response_model=BlogSchema,
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.BLOGS],
    summary="Create a new blog",
    description="Create a new blog entry",
)
async def create_blog(
    blog: BlogCreate,
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> Blog:
    """
    Create a new blog

    Args:
        blog (BlogCreate): The blog data to create
        session (AsyncSession): The async database session dependency

    Returns:
        BlogSchema: The created blog with its assigned id
    """
    new_blog = Blog(
        title=blog.title,
        description=blog.description,
        content=blog.content,
    )
    session.add(new_blog)
    await session.flush()  # Flush to get the auto-generated ID
    await session.refresh(new_blog)  # Refresh to load the ID
    return new_blog


# =============================================================================
# UPDATE Operations
# =============================================================================


@app.put(
    "/update-blog/{blog_id}",
    response_model=BlogSchema,
    status_code=status.HTTP_200_OK,
    tags=[Tags.BLOGS],
    summary="Update a blog",
    description="Update a blog by replacing all its fields",
)
async def update_blog(
    blog_id: int,
    blog: BlogCreate,
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> Blog:
    """
    Update a blog by replacing all its fields.

    Args:
        blog_id: The ID of the blog to update
        blog: The new blog data (title, description, content)

    Returns:
        BlogSchema: The updated blog
    """
    result = await session.execute(select(Blog).where(Blog.id == blog_id))
    existing_blog = result.scalar_one_or_none()
    if existing_blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found",
        )

    existing_blog.title = blog.title
    existing_blog.description = blog.description
    existing_blog.content = blog.content

    await session.flush()
    await session.refresh(existing_blog)
    return existing_blog


@app.patch(
    "/update-blog/{blog_id}",
    response_model=BlogSchema,
    status_code=status.HTTP_200_OK,
    tags=[Tags.BLOGS],
    summary="Partially update a blog",
    description="Partially update a blog - only updates the fields you provide",
)
async def partial_update_blog(
    blog_id: int,
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
    title: str | None = None,
    description: str | None = None,
    content: str | None = None,
) -> Blog:
    """
    Partially update a blog - only updates the fields you provide.

    Args:
        blog_id (int): The ID of the blog to update
        session (AsyncSession): The async database session dependency
        title (str | None): New title (optional)
        description (str | None): New description (optional)
        content (str | None): New content (optional)

    Returns:
        BlogSchema: The updated blog
    """
    # Check if at least one field is provided
    if title is None and description is None and content is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (title, description, or content) must be provided",
        )

    result = await session.execute(select(Blog).where(Blog.id == blog_id))
    existing_blog = result.scalar_one_or_none()
    if existing_blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found",
        )

    # Only update fields that were provided (not None)
    if title is not None:
        existing_blog.title = title
    if description is not None:
        existing_blog.description = description
    if content is not None:
        existing_blog.content = content

    await session.flush()
    await session.refresh(existing_blog)
    return existing_blog


# =============================================================================
# DELETE Operations
# =============================================================================


@app.delete(
    "/delete-blog/{blog_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=[Tags.BLOGS],
    summary="Delete a blog",
    description="Delete a blog by id",
)
async def delete_blog(
    blog_id: int,
    session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> None:
    """
    Delete a blog by id.

    Args:
        blog_id (int): The ID of the blog to delete
        session (AsyncSession): The async database session dependency
    """
    result = await session.execute(select(Blog).where(Blog.id == blog_id))
    existing_blog = result.scalar_one_or_none()
    if existing_blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found",
        )

    await session.delete(existing_blog)
