from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import model
from database import get_db
from model.pydentic_models.user import User

from views import router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/list/", response_model=User)
async def get_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    users = db.query(model.User).all()
    return users
