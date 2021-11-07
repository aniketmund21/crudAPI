from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends 
from fastapi.param_functions import Body
from random import randrange
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
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

#schema for our post request
class Post(BaseModel):#basemodel from pydantic library
    title:str
    content:str
    published:bool = True
    

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

@app.get("/sqlalchemy")
def test_post(db:Session=Depends(get_db)):

    post = db.query(models.Post).all()
    return {"message": post}

@app.get("/posts")
def get_posts(db:Session=Depends(get_db)):
    # older methods
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()

    return {"Data":posts} 

@app.post("/create_post",status_code=status.HTTP_201_CREATED)
def create_post(post: Post,db:Session=Depends(get_db)):
    
    # cursor.execute("""INSERT INTO posts (title,content,published) values (%s,%s,%s) returning * """,(post.title,post.content,post.published))
    # post = cursor.fetchone()
    # conn.commit()
    
    return {"New Post":post}
    


@app.get("/posts/{id}")
def get_post(id):
    
    cursor.execute("""Select * from posts where id = %s """,(id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail=f'No post found with id {id}')
        

    return {"post details": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id):
    cursor.execute("""delete from posts where id=%s returning * """,(id))
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail = f'No post found with id {id}')
   
   
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id,post:Post):
    cursor.execute("""update posts set title=%s,content=%s,published=%s where id =%s returning *"""
    ,(post.title,post.content,post.published,id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail = f'No post found with id {id}')
   
    return {'Data':post}





