from fastapi import FastAPI
from .database import engine

from . import models
from .routers import auth, post, user, vote
from .config import settings


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# HOME PAGE
@app.get('/', tags=["Home"])
async def root():
    return {'message': 'Hello World'}

# AUTH ROUTE
# @app.get('/AUTH', tags=["AUTH"])
# async def auth_route(user_id: int = Depends(oauth2.get_current_user)):
#     pass
