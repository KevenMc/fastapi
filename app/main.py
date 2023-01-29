from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    comment: Optional[int]


while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi',
                                user='postgres',
                                password='Blue.Sky1',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to Postgres Database")
        break
    except Exception as error:
        print("Connection failed with error:")
        print(error)
        time.sleep(2)




#TEST ORM
@app.get('/sqlalchemy')
async def test_posts(db: Session = Depends(get_db)):
    return {'data': "Success"}




#HOME PAGE
@app.get('/')
async def root():
    return {'message': 'Hello World'}


#GET ALL POSTS
@app.get('/posts')
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {'data': posts}


#CREATE POST
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post:Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
                       (post.title,
                        post.content,
                        post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data' : new_post}


#READ POST BY ID
@app.get('/posts/{id}')
def get_post(id:int, response:Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",
                   (str(id)))
    post = cursor.fetchone()
    return {'data': post}


#UPDATE POST BY ID
@app.patch('/posts/{id}')
async def create_post(id:int, post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                       (post.title,
                        post.content,
                        post.published,
                        str(id)))
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post does not exist, perhaps it has been deleted")
    conn.commit()
    return {'data' : updated_post}


#DELETE POST
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",
                   (str(id)))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post does not exist, perhaps it has already been deleted")
    conn.commit()
    return
    