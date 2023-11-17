from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# title: str, content: str we want these things from users
# default value with optional parameter.
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    created_at: datetime
    owner_id: int
    owner: UserOut


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
