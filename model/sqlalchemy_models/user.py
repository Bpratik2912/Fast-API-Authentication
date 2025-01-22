from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

# creates a Base class from DeclarativeBase, serving as the base for all ORM models.
# All models inherit from this Base class. It handles metadata and mapping to the database.
class Base(DeclarativeBase):
    pass


class User(Base):
    # Specifies the name of the table in the database.
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
