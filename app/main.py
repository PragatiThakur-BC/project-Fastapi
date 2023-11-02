from fastapi import FastAPI, status, HTTPException, Response, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schema
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# realdictcursor is going to give us column name as well as the value, will make python dictionary
try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                            password='pragati837', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Connection to database failed")
    print("Error: ", error)


@app.get("/")
async def root():
    return {"message": "API Project with FREECODECAMP"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schema.Post, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # the above code will be difficult to use if we have more in number of fields, so we will unpack the Post
    # schema using model_dump
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return{"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    return_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not return_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found")
    return {"post_detail": return_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# updating all the details of posts
@app.put("/posts/{id}")
def update_post(id: int, post: schema.Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    query_data = post_query.first()
    if query_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    post_query.update(post.model_dump())
    db.commit()
    return {"data": post_query.first()}

