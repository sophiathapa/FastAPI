from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def index():
  return 'hello'

@app.get('/blog/details')
def blog():
  return {'data': "detail"}

@app.get('/blog')
def query(limit = 10 ,published : bool = True, sort : Optional[str] = None):
  if published:
   return {'data':f"{limit} blogs published"}
  else:
    return {'data':f"{limit} blogs not published"}
  
 
@app.get('/blog/{id}')
def detail(id: int):
  return {'id': id}

class Blog(BaseModel):
  title : str
  body : str
  published : Optional[bool]



@app.post('/create')
def create_blog(blog: Blog):
  return {'data':f"blog is created with title : '{blog.title}'"}

