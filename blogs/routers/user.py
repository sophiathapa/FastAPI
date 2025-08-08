from fastapi import status,Depends, APIRouter
from .. import models,schemas
from ..database import get_db
from ..hashing import hash
from sqlalchemy.orm import Session

router = APIRouter(
  prefix='/user',
  tags=['User']
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db : Session = Depends(get_db)):
  new_user = models.User(name = request.name, address = request.address, password = hash.bycrpt(request.password))
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user


@router.get('/',status_code=status.HTTP_200_OK,response_model=list[schemas.ShowUsers])
def getUsers(db : Session = Depends(get_db)):
  users = db.query(models.User).all()
  return users


