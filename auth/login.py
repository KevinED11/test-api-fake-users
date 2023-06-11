from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

from routes.users import get_user

login = APIRouter(tags=["login"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@login.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = 