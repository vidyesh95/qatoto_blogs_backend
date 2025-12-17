from fastapi import FastAPI
from pydantic import BaseModel

myBlogs = {
    "1" : {
        "title": "hello",
        "description": "world",
        "content": "Lorem ipsum The Alola region has no gyms. You can earn the Trio Badge at Striaton Gym. PokéManiac "
                   "visited Goldenrod Department Store in Johto."
    },
    "2" : {
        "title": "hello",
        "description": "world",
        "content": "Lorem ipsum Machop is a Superpower Pokémon. Commander spotted Kangaskhan in Unova. The leader at "
                   "Shalour Gym specializes in Fighting Pokémon. You can find the Eterna Gym in Sinnoh. You can earn "
                   "the Basic Badge at Nacrene Gym."
    },
    "3" : {
        "title": "hello",
        "description": "world",
        "content": "Lorem ipsum Socialite used a Net Ball to catch Victreebel. Tauros used Tail Whip. Voltorb is a "
                   "Ball Pokémon. You can find the Dewford Gym in Hoenn. Haunter used Dream Eater. You can find the "
                   "Fuchsia Gym in Kanto."
    }
}


app = FastAPI()


class Blog(BaseModel):
    title: str
    description: str
    content: str


class Blogs(BaseModel):
    number: int
    blog: Blog


def get_blog(blog: Blog):
    return blog.title, blog.content


def get_blogs(title: str, description: str):
    return title, description

print(get_blogs("hello","world"))
print(get_blog(Blog("hello","world","Lorem ipsum The Alola region has no gyms. You can earn the Trio Badge at Striaton "
                       "Gym. PokéManiac visited Goldenrod Department Store in Johto.")))