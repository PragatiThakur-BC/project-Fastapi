from typing import Dict
from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

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
    # till here the api will give us o/p of new post we added, but it will not add this to database we have to
    # commit() with connection. All the above code creates staged changes and below one commits to DB.
    conn.commit()
    return{"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id))
    return_post = cursor.fetchone()
    if not return_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found")
    return {"post_detail": return_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, str(id))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# updating all the details of posts
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    return {"data": updated_post}
