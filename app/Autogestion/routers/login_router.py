# Imports libraries
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
import re


# Imports
# Models
from app.Autogestion.models.login_model import loginModel
# Controllers
from app.Autogestion.controllers.login_controller import login_controller


# APP Router
router = APIRouter(prefix='/login')


# APP token_access
oauth2 = OAuth2PasswordBearer(tokenUrl="/login")


# Routers ------------------------------------------------------------------------------>
# Valida el modelo de los datos y el dominio del correo.
@router.post('/')
async def login_router(login: loginModel):
    patron_gmail = re.compile(r'^[a-zA-Z0-9_.+-]+@clinicos\.com\.co$')
    if patron_gmail.match(login.correo):
        user = await login_controller(login)
        return user
    else:
        return "Correo no valido"
