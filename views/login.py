from datetime import timedelta, datetime
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import model
from database import get_db
from model.pydentic_models import UserPassword, UserToken
from views.signup import router

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
        Verifies if the plain password matches the hashed password.

        Args:
        - plain_password (str): The password entered by the user.
        - hashed_password (str): The hashed password stored in the database.

        Returns:
        - bool: True if the passwords match, False otherwise.
    """

    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str):
    """
        Retrieves a user from the database by username.

        Args:
        - db (Session): The database session.
        - username (str): The username to search for.

        Returns:
        - UserPassword: A Pydantic model containing the user details, or None if not found.
    """

    user = db.query(model.User).filter(model.User.user_name == username).first()
    if user:
        return UserPassword(**user.__dict__)

def authenticate_user(db, username: str, password: str):
    """
       Authenticates a user by verifying their username and password.

       Args:
       - db (Session): The database session.
       - username (str): The username.
       - password (str): The password.

       Returns:
       - UserPassword: The authenticated user model if valid, False if authentication fails.
    """

    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_token(data: dict, expires_delta: timedelta | None = None):
    """
       Creates a JWT access token for the user.

       Args:
       - data (dict): The payload data to be encoded into the JWT.
       - expires_delta (timedelta | None): The token expiration time.

       Returns:
       - str: The encoded JWT token.
    """

    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login/")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """
        Handles the login process by authenticating the user and returning a JWT access token.

        Args:
        - form_data (OAuth2PasswordRequestForm): The login form containing username and password.
        - db (Session): The database session.

        Returns:
        - UserToken: A Pydantic model containing the access token and token type.

        Raises:
        - HTTPException: If authentication fails with a 401 status.
    """

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_token(
        data={"sub": user.user_name}, expires_delta=timedelta(days=1)
    )
    refresh_token = create_token(
        data={"sub": user.user_name}, expires_delta=timedelta(days=5)
    )
    return UserToken(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
