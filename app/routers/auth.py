from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from .. import schemas, models, utils, oauth2


router = APIRouter(tags=["Authentication"])


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(
        models.User.email == user_credentials.username)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Login credentials are not valid. Have you forgot your email or password?")

    if not utils.Verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Login credentials are not valid. Have you forgot your email or password?")

    user_query.update({'last_logged_in': datetime.now()},
                      synchronize_session=False)
    db.commit()

    access_token = oauth2.create_access_toke(data={"user_id": user.id})

    return {'access_token': str(access_token), "token_type": "Bearer"}
