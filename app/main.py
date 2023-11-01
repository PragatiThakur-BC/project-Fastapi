from typing import Optional, Dict
from fastapi import FastAPI, status, HTTPException, Response
# from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()


# title: str, content: str we want these things from users
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default value with optional parameter.


# realdictcursor is going to give us column name as well as the value, will make python dictionary

try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                            password='pragati837', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Connection to database failed")
    print("Error: ", error)


# Since we are not using database to assign an id we will have to use random package
my_posts = [{"id": 1, "title": "title of post1", "content": "content of post1"},
            {"id": 2, "title": "A world of Coffee's",
             "content": "Different flavoured Coffee's with different methods to make them."}]


@app.get("/")
async def root():
    return {"message": "API Project with FREECODECAMP"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES({post.title},
    # {post.content},{post.content})") This way can cause sql injection as user can give any random title or info here
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    # till here the api will give use o/p of new post we added, but it will not add this to database we have to
    # commit() with connection. All the above code creates staged changes and below one commits to DB.
    conn.commit()
    return{"data": new_post}


# retrieving one individual post via id and this to search that post
def find_post(id) -> Dict:
    for p in my_posts:
        if p['id'] == id:
            return p


@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found")

    return {"post_detail": post}


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# updating all the details of posts
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
