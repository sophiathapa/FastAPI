from pydantic import BaseModel

class Blog(BaseModel):
  title: str
  body: str

class User(BaseModel):
  name: str
  address: str
  password:str

class ShowUsers(BaseModel):
  name : str
  address: str
  class config():
    orm_mode = True

class ShowBlog(BaseModel):
  title: str
  body : str
  creator : ShowUsers
  class config():
    orm_mode = True

