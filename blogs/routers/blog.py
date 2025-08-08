from fastapi import HTTPException, Depends, status,APIRouter 
from .. import models, schemas 
from ..oauth2 import get_current_user
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix='/blog',
  tags=['Blog']
)

@router.post('/',status_code= status.HTTP_201_CREATED)
def create(request : schemas.Blog, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
  new_blog = models.Blog(title = request.title , body=request.body, user_id = 1)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog


@router.get('/',response_model=list[schemas.ShowBlog])
def all(db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
  blog = db.query(models.Blog).all()
  return blog

@router.get('/{id}',response_model= schemas.ShowBlog)
def show(id, db: Session= Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog with id {id} is not available")
  
  return blog


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def remove(id,db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog with id {id} is not available")
  blog.delete(synchronize_session=False)
  db.commit()
  return f"the blog of id {id} is deleleted"

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request: schemas.Blog, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog with id {id} is not available")
  blog.update(request.dict())
  db.commit()
  return f"The blog with id {id} is Updated"