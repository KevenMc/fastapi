from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional


#######################################################
# TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


#####################################################################
#USERS
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserReturn(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        orm_mode = True

#####################################################################
# VOTE


class Vote(BaseModel):
    post_id: int
    
#####################################################################
# POSTS
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserReturn

    class Config:
        orm_mode = True


class PostVotes(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True
