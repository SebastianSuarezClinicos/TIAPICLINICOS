

from fastapi import APIRouter, Header, Response
from app.Autogestion.controllers.verification_controller import verify_code

from app.Autogestion.models.verification_model import VerificationModel


router = APIRouter(prefix='/Autogestion')

@router.post('/TestCookie', summary="Enviar código de verificación", response_description="Resultado del envío")
async def sHello(
    #verification_data: VerificationModel,verification_data
    response: Response,
    #authorization: str = Header(None), authorization, authorization
    ):
    hello = "Hello World"

    #verify_code_response = await verify_code()
    # Establecer la cookie con el token JWT
    #response.set_cookie(key="accessToken", value=verify_code_response["token"], httponly=True, secure=True, samesite='None', max_age=1800, domain=None)

    response.set_cookie(key="hello", value=hello, httponly=True, secure=True, samesite='None', max_age=1800, domain=None)
    return {
        "message": "Verificacion exitosa",
        "data": hello,
        "headers": {"set-cookie": "accessToken=1234"}
    }#verify_code_response["history_result"]),