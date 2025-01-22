from fastapi import APIRouter, Depends, status, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import model
from database import get_db, session
from model.pydentic_models.user import User
from pydantic import ValidationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/user", tags=["Users"])

def get_password_hash(password):
    """
        Hashes a plain password using bcrypt.

        Args:
        - password (str): The plain password to hash.

        Returns:
        - str: The hashed password.
    """

    return pwd_context.hash(password)

@router.post("/signup/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User, db: Session = Depends(get_db)):
    """
        Create a new user in the database.

        This function checks whether a user with the provided email already exists.
        If not, it hashes the password and creates a new user record in the database.

        Args:
        - user (User): The user data for creating a new user.
        - db (Session): The database session.

        Returns:
        - JSONResponse: A JSON response indicating the success of the user creation.

        Raises:
        - HTTPException: If a user with the same email already exists or if any validation errors occur.
    """

    try:
        # Check if the email already exists in the database.
        existing_user = db.query(model.User).filter(model.User.email==user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

        # Create the new user object and hash the password.
        user_db = model.User(
            user_name=user.user_name,
            email=user.email,
            password=get_password_hash(user.password),
            is_active=True,
        )

        # Add the new user to the database and commit the transaction
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
    except ValidationError as e:
        # Raise an HTTPException with a 422 status code if validation fails
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e.errors()))

    # Return a success response with a message
    return JSONResponse(content={"message": "User created successfully."}, media_type='application/json')
