# imports libraries
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from decouple import config
import httpx
from app.Autogestion.controllers.write_list_controller import write_list


# Imports
# db
from db.client_graph import get_access_token
# Models
from app.Autogestion.models.login_model import loginModel




# Creación de token de acceso ---------------------------------------------------------------->
# Constantes de acceso
SECRET_KEY = config('SECRET_KEY')
ALGORITHM =  config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))

# Creación de token
def create_access_token(data: dict, expires_delta: int):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Environment variables
site = config('SITE_AGENDAMIENTO_ECOPETROL')
sub_site = config('SUBSITE_MEGAS_BULEVAR')
list_id = config('LIST_POBLACION')

# CONTROLLER
async def login_controller(login: loginModel):
    try:
        # db access token
        token = await get_access_token()

        # Parameters
        tidentificacion = login.tipodeidentificacion
        nidentificacion = login.numerodeidentificacion
        correo = login.correo

        # Configuration URL
        URL = f'https://graph.microsoft.com/v1.0/sites/{site}/sites/{sub_site}/lists/{list_id}/items'
        headers = {"Authorization": f"Bearer {token}"}

        filter_query = {'$filter': f"fields/Title eq '{nidentificacion}' and fields/TipodeIdentificaci_x00f3_n eq '{tidentificacion}' and fields/E_x002d_mail eq '{correo}' ",
                        "$expand": "fields"}

        # HTTP request
        async with httpx.AsyncClient() as client:
            response = await client.get(URL, headers=headers, params=filter_query)
            response.raise_for_status
            users = response.json()
            #print(users)

    # Exception de la respuesta json
    except httpx.RequestError as e:
        raise HTTPException(status_code=500,
                            detail=f"Error en la solicitud HTTP: {e}")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=response.status_code,
                            detail=f"Error en la respuesta HTTP: {e}")

    except ValueError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al analizar JSON: {e}")


    # Response
    if users.get("value", []) == []:
        return "Usuario no encontrado"
    else:
        Identificacion= users["value"][0]["fields"]["Title"]
        Tipo_Identificacion = users["value"][0]["fields"]["TipodeIdentificaci_x00f3_n"]
        estado = users["value"][0]["fields"]["Estado"]
        nombres = users["value"][0]["fields"]["Nombres"]
        apellidos = users["value"][0]["fields"]["Apellidos"]
        ingreso = "Pendiente"
        #print(list_id)

        if estado != "ACTIVO/A":
            return "Usuario Inactivo"
        access_token_expires = ACCESS_TOKEN_EXPIRE_MINUTES
        access_token = create_access_token(data={"Tidentidad": Tipo_Identificacion, "Nidentidad": Identificacion}, expires_delta=access_token_expires)
        #return users

        result_write_list = await write_list(
        access_token=access_token,
        correo=correo,
        nombres=nombres,
        apellidos=apellidos,
        tipo_identificacion=Tipo_Identificacion,
        numero_identificacion=Identificacion,
        ingreso=ingreso
    )
        return result_write_list
        #return {"access_token": access_token, "token_type": "bearer"}
