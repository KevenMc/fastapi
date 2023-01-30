from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List

from .. import models, schemas, oauth2
from ..database import engine, get_db


router = APIRouter(prefix='/posts',
                   tags=["Posts"],)


# CREATE POST
@router.post('/',
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.PostResponse,
             summary="Create a Post",
             description="Creates a new post")
async def create_post(post: schemas.PostCreate,
                      db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(user_id=current_user.id,
                           **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# READ POST BY ID
@router.get('/{id}',
            response_model=schemas.PostResponse)
def get_post(id: int,
             response: Response,
             db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post does not exist, perhaps it has been deleted")

    return post


# GET ALL POSTS
@router.get('/',
            response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# UPDATE POST BY ID
@router.patch('/{id}',
              response_model=schemas.PostResponse)
async def create_post(id: int,
                      update_post: schemas.PostCreate,
                      db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post does not exist, perhaps it has been deleted")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Oops, you can't do this")
        
    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


# DELETE POST
@router.delete('/{id}',
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,
                      db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if  post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post does not exist, perhaps it has been deleted")
        
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Oops, you can't do this")
        
    post_query.delete(synchronize_session=False)
    db.commit()
    return
