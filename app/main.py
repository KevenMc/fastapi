from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Set up database
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


# HOME PAGE
@app.get('/')
async def root():
    return {'message': 'Hello World'}


# GET ALL POSTS
@app.get('/posts', response_model = List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


# CREATE POST
@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model = schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                    (post.title,
    #                     post.content,
    #                     post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(title = post.title,
                           content = post.content,
                           published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# READ POST BY ID
@app.get('/posts/{id}', response_model = schemas.PostResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",
    #                (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail="This post does not exist, perhaps it has been deleted")
    return post


# UPDATE POST BY ID
@app.patch('/posts/{id}', response_model = schemas.PostResponse)
async def create_post(id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                    (post.title,
    #                     post.content,
    #                     post.published,
    #                     str(id)))
    # updated_post = cursor.fetchone()
    # if updated_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail="This post does not exist, perhaps it has been deleted")
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail="This post does not exist, perhaps it has been deleted")
    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


# DELETE POST
@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",
    #                (str(id)))
    # post = cursor.fetchone()
    # if post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail="This post does not exist, perhaps it has already been deleted")
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post does not exist, perhaps it has been deleted")
    post_query.delete(synchronize_session=False)
    db.commit()
    return
