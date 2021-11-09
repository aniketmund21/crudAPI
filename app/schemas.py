from pydantic import BaseModel

#schema for our post request

class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True

class PostCreate(PostBase):
    pass
