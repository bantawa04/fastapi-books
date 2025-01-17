from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import List
from src.books.schema import Book
from src.db.models import Review


class User(BaseModel):
    uid: uuid.UUID
    first_name: str
    last_name: str
    username: str
    password: str = Field(exclude=True)
    email: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserBooksModel(User):
    books: List[Book]
    reviews: List[Review]


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    username: str = Field(min_length=5)
    password: str = Field(min_length=5)
    email: str = Field(min_length=6)


class UpdateUserRequest(BaseModel):
    first_name: str
    last_name: str
    username: str = Field(max_length=8)
    password: str = Field(max_length=40)
    email: str = Field(min_length=6)


class LoginRequest(BaseModel):
    email: str
    password: str
