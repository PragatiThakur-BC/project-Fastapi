from pydantic import BaseModel, EmailStr
from datetime import datetime


# title: str, content: str we want these things from users
# default value with optional parameter.
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    created_at: datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

