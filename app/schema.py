from pydantic import BaseModel


# title: str, content: str we want these things from users
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default value with optional parameter.
