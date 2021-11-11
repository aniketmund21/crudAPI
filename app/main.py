from typing import Optional,List
from fastapi import FastAPI,Response,status,HTTPException,Depends 
from fastapi.param_functions import Body
from random import randrange
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine, get_db



models.Base.metadata.create_all(bind=engine)
#use uvicorn app.main:app --reload to start the server

app = FastAPI()



#connecting to our database
while True:
    try:
        conn = psycopg2.connect(host ='localhost',database ='FastAPI'
                        ,user ='postgres',password='aniket01',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print ("Connection Was Successful")
        break

    except Exception as error:
        print ("Connection Failed")
        print ("Error: ", error)      
        time.sleep(2)              


    

my_posts = [{"title":"I am iron man","content":"i am content","id":"1",},{"title":"Hey Baby", "content":"I am content 2","id":"2"}]

def find_post(id):
    for p in my_posts:
        if p['id']== id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id']== id:
            return i            

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db)):
    # older methods
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()

    return posts

@app.post("/create_post",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db:Session=Depends(get_db)):
    
    # cursor.execute("""INSERT INTO posts (title,content,published) values (%s,%s,%s) returning * """,(post.title,post.content,post.published))
    # post = cursor.fetchone()
    # conn.commit()

    #post.dict will solve manual problem of entering rhe fields
    # post = models.Post(title=post.title,content=post.content,published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post 
    


@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id,db:Session=Depends(get_db)):
    
    # cursor.execute("""Select * from posts where id = %s """,(id))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail=f'No post found with id {id}')
        

    return {"post details": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id,db:Session=Depends(get_db)):
    # cursor.execute("""delete from posts where id=%s returning * """,(id))
    # deleted_post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail = f'No post found with id {id}')
    
    post.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id,post:schemas.PostBase,db:Session=Depends(get_db)):
    # cursor.execute("""update posts set title=%s,content=%s,published=%s where id =%s returning *"""
    # ,(post.title,post.content,post.published,id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail = f'No post found with id {id}')
    
    updated_post= post_query.update(post.title, post.content)
    db.commit()
    return {'Data':updated_post}


@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



