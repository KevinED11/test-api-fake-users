from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

from routes.users import get_user, get_cached_users

login = APIRouter(tags=["login"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

