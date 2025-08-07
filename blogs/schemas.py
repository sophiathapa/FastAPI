from pydantic import BaseModel

class BaseBlog(BaseModel):
  title: str
  body: str

class Blog(BaseBlog):
  def config():
    orm_mode = True
    
class User(BaseModel):
  name: str
  address: str
  password:str

class ShowUsers(BaseModel):
  name : str
  address: str
  blogs: list[Blog] = []
  class config():
    orm_mode = True

class ShowBlog(BaseModel):
  title: str
  body : str
  creator : ShowUsers
  class config():
    orm_mode = True

