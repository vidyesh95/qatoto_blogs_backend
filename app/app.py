from enum import Enum
from typing import Annotated, TypedDict

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

description = """
Qatoto Blogs API

Qatoto Blogs is a simple API for managing blogs.
"""

app = FastAPI(
    title="Qatoto Blogs",
    description=description,
    summary="Qatoto Blogs API",
    version="0.0.1",
)


class Blog(BaseModel):
    blog_id: int
    title: str
    description: str
    content: str


class BlogCreate(BaseModel):
    title: str
    description: str
    content: str


class Blogs(BaseModel):
    blog: Blog


class BlogResponse(BaseModel):
    blog_id: int
    title: str
    content: str


class BlogsResponse(BaseModel):
    blog_id: int
    title: str
    description: str


class BlogTable(TypedDict):
    blog_id: int
    title: str
    description: str
    content: str


db: list[BlogTable] = [
    {
        "blog_id": 1,
        "title": "hello",
        "description": "world",
        "content": "Lorem ipsum The Alola region has no gyms. You can earn the Trio Badge at Striaton Gym. PokéManiac "
        "visited Goldenrod Department Store in Johto.",
    },
    {
        "blog_id": 2,
        "title": "hello2",
        "description": "world2",
        "content": "Lorem ipsum Machop is a Superpower Pokémon. Commander spotted Kangaskhan in Unova. The leader at "
        "Shalour Gym specializes in Fighting Pokémon. You can find the Eterna Gym in Sinnoh. You can earn "
        "the Basic Badge at Nacrene Gym.",
    },
    {
        "blog_id": 3,
        "title": "hello3",
        "description": "world3",
        "content": "Lorem ipsum Socialite used a Net Ball to catch Victreebel. Tauros used Tail Whip. Voltorb is a "
        "Ball Pokémon. You can find the Dewford Gym in Hoenn. Haunter used Dream Eater. You can find the "
        "Fuchsia Gym in Kanto.",
    },
]


async def find_blog_by_id(target_blog_id: int) -> BlogTable | None:
    """
    Search through the database list and return the blog that matches the target_blog_id.
    Returns None if no matching blog is found.
    """
    for blog_entry in db:
        if blog_entry["blog_id"] == target_blog_id:
            return blog_entry
    return None


async def read_blog(blog_id: int) -> Blog:
    # Find the blog with matching blog_id
    blog = await find_blog_by_id(blog_id)
    if blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found",
        )

    return Blog(
        blog_id=blog["blog_id"],
        title=blog["title"],
        description=blog["description"],
        content=blog["content"],
    )


async def read_blogs() -> list[Blog]:
    if not db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No blogs found",
        )

    return [
        Blog(
            blog_id=blog["blog_id"],
            title=blog["title"],
            description=blog["description"],
            content=blog["content"],
        )
        for blog in db
    ]


class Tags(Enum):
    blogs = "blogs"
    auth = "auth"


@app.get(
    "/blog/{blog_id}",
    response_model=BlogResponse,
    tags=[Tags.blogs],
    summary="Read a blog",
    description="Read a blog by id",
    response_description="The blog with the given id",
)
async def get_blog(blog_id: Annotated[int, "Enter the blog id to read the blog"]):
    """
    Read a blog by id

    Args:
        blog_id (int): The id of the blog to read

    Returns:
        Blog: The blog with the given id
    """
    result = await read_blog(blog_id)
    return result


@app.get(
    "/",
    response_model=list[BlogsResponse],
    tags=[Tags.blogs],
    summary="Read all blogs",
    description="Read all blogs",
    response_description="List of all blogs",
)
async def get_blogs():
    """
    Read all blogs

    Returns:
        list[BlogsResponse]: List of all blogs
    """
    results = await read_blogs()
    return results


async def add_blog_to_db(blog: BlogCreate) -> Blog:
    """
    Create a new blog entry and add it to the database.
    Auto-generates a unique blog_id.

    Args:
        blog: The blog data to create (title, description, content)

    Returns:
        Blog: The created blog with its assigned blog_id
    """
    # Auto-generate a unique blog_id
    existing_blog_ids = [blog_entry["blog_id"] for blog_entry in db]
    highest_existing_id = max(existing_blog_ids) if existing_blog_ids else 0
    new_blog_id = highest_existing_id + 1
    new_blog: BlogTable = {
        "blog_id": new_blog_id,
        "title": blog.title,
        "description": blog.description,
        "content": blog.content,
    }
    db.append(new_blog)
    return Blog(**new_blog)


@app.post("/create-blog", status_code=status.HTTP_201_CREATED, tags=[Tags.blogs])
async def create_blog(blog: BlogCreate) -> Blog:
    """
    Create a new blog

    Args:
        blog (BlogCreate): The blog data to create

    Returns:
        Blog: The created blog
    """
    return await add_blog_to_db(blog)


@app.put("/update-blog/{blog_id}", status_code=status.HTTP_200_OK, tags=[Tags.blogs])
async def update_blog(blog_id: int, blog: Blog):
    return {"blog_id": blog_id, "blog": blog}


@app.patch(
    "/partial-update-blog/{blog_id}", status_code=status.HTTP_200_OK, tags=[Tags.blogs]
)
async def partial_update_blog(blog_id: int, blog: Blog):
    return {"blog_id": blog_id, "blog": blog}


@app.delete(
    "/delete-blog/{blog_id}", status_code=status.HTTP_204_NO_CONTENT, tags=[Tags.blogs]
)
async def delete_blog(blog_id: int):
    return status.HTTP_204_NO_CONTENT
