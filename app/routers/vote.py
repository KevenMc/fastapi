from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(prefix='/vote',
                   tags=["Vote"],)


def checkPost(post_id: int,
              db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(
        models.Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post does not exist")


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,
         db: Session = Depends(get_db),
         current_user: int = Depends(oauth2.get_current_user)):
    
    checkPost(vote.post_id, db)
    
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if found_vote:
        vote_query.delete()
    else:
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
    db.commit()


@router.get('/{post_id}')
def vote(post_id: int,
         db: Session = Depends(get_db),
         current_user: int = Depends(oauth2.get_current_user)):

    checkPost(post_id, db)
    votes = db.query(models.Vote).filter(
        models.Vote.post_id == post_id).all()

    has_voted = False

    voted = db.query(models.Vote).filter(
        models.Vote.post_id == post_id, models.Vote.user_id == current_user.id).first()
    if voted:
        has_voted = True

    return {"vote_count": len(votes), "voted": has_voted}
