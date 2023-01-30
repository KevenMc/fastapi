from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import  get_db


router = APIRouter(prefix='/users')

# CREATE USER
@router.post('/', status_code=status.HTTP_201_CREATED,  response_model=schemas.UserReturn)
async def create_post(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This Email address ishas an account. Have you forgotten your password?")
    
    user.password = utils.Hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#GET USER BY ID
@router.get('/{id}', response_model=schemas.UserReturn)
def get_user(id: int, db: Session = Depends(get_db),):
    user = db.query(models.User).filter(models.User.id == int(id)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This User does not existd")
    return user
