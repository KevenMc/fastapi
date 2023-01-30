from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List

from .. import models, schemas
from ..database import engine, get_db


router = APIRouter(prefix='/posts')


# CREATE POST
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title,
                           content=post.content,
                           published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# READ POST BY ID
@router.get('/{id}', response_model=schemas.PostResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post does not exist, perhaps it has been deleted")
    return post


# GET ALL POSTS
@router.get('/', response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# UPDATE POST BY ID
@router.patch('/{id}', response_model=schemas.PostResponse)
async def create_post(id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post does not exist, perhaps it has been deleted")
    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


# DELETE POST
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post does not exist, perhaps it has been deleted")
    post_query.delete(synchronize_session=False)
    db.commit()
    return