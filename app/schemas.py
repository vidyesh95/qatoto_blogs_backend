"""
This file mainly contains Pydantic schemas for models, used for validation and serialization.
"""
from typing import TypedDict

from pydantic import BaseModel


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
