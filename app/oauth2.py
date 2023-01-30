from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import uuid


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "7fce70c4-914c-4cb0-a403-efc4a61c8c657d85e4ae-a0d9-11ed-a8fc-0242ac120002"
#SECRET_KEY = str(uuid.uuid1()) + str(uuid.uuid1())

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


def create_access_toke(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode,
                      SECRET_KEY,
                      ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token,
                             SECRET_KEY,
                             algorithms=[ALGORITHM])

        id = payload.get("user_id")

        if not id:
            raise credentials_exception

        token_data = schemas.TokenData(id=str(id))

        return token_data

    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not log in",
                                          headers={
                                              "WWW-Authenticate": "Bearer"}
                                          )
    return verify_access_token(token, credentials_exception)
