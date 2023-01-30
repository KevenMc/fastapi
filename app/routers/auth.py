from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from .. import schemas, models, utils





router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    
    user_query = db.query(models.User).filter(models.User.email == user_credentials.email)
    user = user_query.first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Login credentials are not valid. Have you forgot your email or password?")
    
    if not utils.Verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Login credentials are not valid. Have you forgot your email or password?")
    
    user_query.update({'last_logged_in': datetime.now()}, synchronize_session=False)
    db.commit()

    return {'token': "token"}