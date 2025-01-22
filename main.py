from fastapi import FastAPI

from fastapi.security import OAuth2PasswordBearer

from views.signup import router

# Define the authentication scheme. the endpoint where users will submit
# their credentials to obtain an access token (e.g., /login route).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Creates an instance of FastAPI, representing the core application.
app = FastAPI()

# register the router for the application
app.include_router(router=router)

