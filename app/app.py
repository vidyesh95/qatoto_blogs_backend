from typing import Annotated, TypedDict

from fastapi import FastAPI
from pydantic import BaseModel


class BlogEntry(TypedDict):
    blog_id: int
    title: str
    description: str
    content: str


db: list[BlogEntry] = [
    {
        "blog_id": 1,
        "title": "hello",
        "description": "world",
        "content": "Lorem ipsum The Alola region has no gyms. You can earn the Trio Badge at Striaton Gym. PokéManiac "
        "visited Goldenrod Department Store in Johto.",
    },
    {
        "blog_id": 2,
        "title": "hello",
        "description": "world",
        "content": "Lorem ipsum Machop is a Superpower Pokémon. Commander spotted Kangaskhan in Unova. The leader at "
        "Shalour Gym specializes in Fighting Pokémon. You can find the Eterna Gym in Sinnoh. You can earn "
        "the Basic Badge at Nacrene Gym.",
    },
    {
        "blog_id": 3,
        "title": "hello",
        "description": "world",
        "content": "Lorem ipsum Socialite used a Net Ball to catch Victreebel. Tauros used Tail Whip. Voltorb is a "
        "Ball Pokémon. You can find the Dewford Gym in Hoenn. Haunter used Dream Eater. You can find the "
        "Fuchsia Gym in Kanto.",
    },
]


app = FastAPI()


class Blog(BaseModel):
    blog_id: int
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


async def read_blog(blog_id: int) -> Blog:
    return Blog(
        blog_id=blog_id,
        title=db[blog_id]["title"],
        description=db[blog_id]["description"],
        content=db[blog_id]["content"],
    )


async def read_blogs() -> list[Blog]:
    return [
        Blog(
            blog_id=blog["blog_id"],
            title=blog["title"],
            description=blog["description"],
            content=blog["content"],
        )
        for blog in db
    ]


@app.get("/blog/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: Annotated[int, "Enter the blog id to read the blog"]):
    result = await read_blog(blog_id)
    return result


@app.get("/", response_model=list[BlogsResponse])
async def get_blogs():
    results = await read_blogs()
    return results


# @app.post("/create-blog", response_model=Blog)
# async def create_blog(blog: Blog):
#     return BlogResponse(
#         blog_id=len(db) + 1,
#         title=blog.title,
#         description=blog.description,
#         content=blog.content,
#     )
