from typing import Optional
from fastapi import FastAPI
from fastapi.param_functions import Body

from pydantic import BaseModel
#use uvicorn main:app --reload to start the server

app = FastAPI()

#schema for our post request
class Post(BaseModel):#basemodel from pydantic library
    title:str
    content:str
    published:bool = True
    rating:Optional[float] = None

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/post")
def get_posts():
    return {"Data": "My Post"} 

@app.post("/create_post")
def create_post(post: Post):
    print(post.rating)
    post.dict
    return {"New Post":post}
    

# we want a title which is astring and content also a string so we use pydantic for a schema
#title str , content str