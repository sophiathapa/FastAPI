from fastapi import FastAPI,Depends,status, HTTPException , Request
from . import models, schemas
from .database import engine,SessionLocal
from sqlalchemy.orm import Session 
from .hashing import hash

app = FastAPI()
models.Base.metadata.create_all(engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@app.post('/blog',status_code= status.HTTP_201_CREATED, tags=['Blog'])
def create(request : schemas.Blog, db: Session = Depends(get_db)):
  new_blog = models.Blog(title = request.title , body=request.body, user_id = 1)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog


@app.get('/blog',response_model=list[schemas.ShowBlog], tags=['Blog'])
def all(db: Session = Depends(get_db)):
  blog = db.query(models.Blog).all()
  return blog

@app.get('/blog/{id}',response_model= schemas.ShowBlog,tags=['Blog'])
def show(id, db: Session= Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog with id {id} is not available")
  
  return blog


@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
def remove(id,db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog with id {id} is not available")
  blog.delete(synchronize_session=False)
  db.commit()
  return f"the blog of id {id} is deleleted"

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED, tags=['Blog'])
def update(id,request: schemas.Blog, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog with id {id} is not available")
  blog.update(request.dict())
  db.commit()
  return f"The blog with id {id} is Updated"


@app.post('/user',status_code=status.HTTP_201_CREATED, tags=['User'])
def create_user(request: schemas.User, db : Session = Depends(get_db)):
  new_user = models.User(name = request.name, address = request.address, password = hash.bycrpt(request.password))
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user


@app.get('/users',status_code=status.HTTP_200_OK,response_model=list[schemas.ShowUsers], tags=['User'])
def getUsers(db : Session = Depends(get_db)):
  users = db.query(models.User).all()
  return users


