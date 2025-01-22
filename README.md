# FastAPI User Authentication API

This is a simple FastAPI-based application providing user authentication functionality, including signup and login features using JWT tokens. The application connects to a PostgreSQL database and leverages SQLAlchemy ORM for database operations. Passwords are hashed with bcrypt, ensuring secure storage.

## Features

- **User Signup**: Allows users to register with a username, email, and password.
- **User Login**: Allows users to log in using their credentials and obtain JWT access and refresh tokens.
- **JWT Token Authentication**: Secures routes that require authenticated access using JWT tokens.

## Technologies Used

- **FastAPI**: A modern web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **SQLAlchemy**: ORM for database interactions with PostgreSQL.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **bcrypt**: A hashing function used to securely store user passwords.
- **JWT**: JSON Web Tokens used for securely transmitting information between users and the API.
- **PostgreSQL**: Relational database used to store user data.
