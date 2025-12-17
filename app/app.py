from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel

db = {
    1: {
        "title": "hello",
        "description": "world",
        "content": "Lorem ipsum The Alola region has no gyms. You can earn the Trio Badge at Striaton Gym. PokéManiac "
        "visited Goldenrod Department Store in Johto.",
    },
    2: {
        "title": "hello",
        "description": "world",
        "content": "Lorem ipsum Machop is a Superpower Pokémon. Commander spotted Kangaskhan in Unova. The leader at "
        "Shalour Gym specializes in Fighting Pokémon. You can find the Eterna Gym in Sinnoh. You can earn "
        "the Basic Badge at Nacrene Gym.",
    },
    3: {
        "title": "hello",
        "description": "world",
        "content": "Lorem ipsum Socialite used a Net Ball to catch Victreebel. Tauros used Tail Whip. Voltorb is a "
        "Ball Pokémon. You can find the Dewford Gym in Hoenn. Haunter used Dream Eater. You can find the "
        "Fuchsia Gym in Kanto.",
    },
}


app = FastAPI()


class Blog(BaseModel):
    id: int
    title: str
    description: str
    content: str


class Blogs(BaseModel):
    blog: Blog


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str


class BlogsResponse(BaseModel):
    id: int
    title: str
    description: str


async def read_blog(id: int) -> Blog:
    return Blog(
        id=id,
        title=db[id]["title"],
        description=db[id]["description"],
        content=db[id]["content"],
    )


async def read_blogs() -> list[Blog]:
    return [
        Blog(
            id=id,
            title=blog["title"],
            description=blog["description"],
            content=blog["content"]
        ) 
        for id, blog in db.items()
    ]


@app.get("/blog/{id}", response_model=BlogResponse)
async def get_blog(id: Annotated[int, "Enter the blog id to read the blog"]):
    result = await read_blog(id)
    return result


@app.get("/", response_model=list[BlogsResponse])
async def get_blogs():
    results = await read_blogs()
    return results
