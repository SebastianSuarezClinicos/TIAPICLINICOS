

from fastapi import APIRouter, Header, Response


router = APIRouter(prefix='/Autogestion')

@router.post('/TestCookie', summary="Enviar código de verificación", response_description="Resultado del envío")
async def sHello(response: Response,
    authorization: str = Header(None)):
    hello = "Hello World"
    response.set_cookie(key="hello", value=hello, httponly=True, secure=True, samesite='None', max_age=1800, domain=None)
    return hello, authorization