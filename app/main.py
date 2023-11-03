from fastapi import FastAPI, status, HTTPException, Response, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schema, services
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from .routers import post, user

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

app.include_router(post.router)
app.include_router(user.router)





