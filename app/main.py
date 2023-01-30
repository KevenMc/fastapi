from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine

from . import models
from .routers import post, user, auth


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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)



# HOME PAGE
@app.get('/', tags=["Home"])
async def root():
    return {'message': 'Hello World'}
