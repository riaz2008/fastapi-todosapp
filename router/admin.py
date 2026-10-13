from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session  
from datetime import datetime, timedelta, timezone
from typing import Annotated
from database import SessionLocal
from models import Users 
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
# from router.auth import admin
from models import Todos
from router.auth import get_current_user


router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAuth2_bearer = OAuth2PasswordBearer(tokenUrl='login')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/admin/todo')
def read_todos(user : user_dependency, db : db_dependency):

    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail = 'Failed Authentication')

    return db.query(Todos).all()

@router.delete('/admin/delete/{todo_id}')
def delete_todos_by_admin(user : user_dependency, db : db_dependency, todo_id : int):

    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code = 404,detail = 'Failed authentication')

    todo = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=404,detail='To do not found')
    
    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()
    return JSONResponse(status_code=200,content="To do deleted successfully")


