from fastapi import APIRouter, Depends, status, HTTPException
from ..schemas import Login
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..hashing import hash
from ..token import create_access_token


router = APIRouter(
  prefix='/login',
  tags=['Authentication']
)

@router.post('/',status_code=status.HTTP_200_OK)
def login(request: Login , db : Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.name == request.username).first()
  if not user :
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = 'Invalid Credentials')
  
  if not hash.verify(request.password, user.password):
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = 'Incorrect Password')
  
  access_token = create_access_token(data={"sub": user.name})
  return {'access_token':access_token, 'token_type':"bearer"}

 

