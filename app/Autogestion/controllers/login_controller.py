# imports libraries
from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta
from decouple import config
import httpx
from app.Autogestion.controllers.verification_controller import send_verification_code_route
from app.Autogestion.controllers.write_list_controller import write_list
from app.Autogestion.services.token_User import create_access_token
# Imports
# db
from db.client_graph import get_access_token
# Models
from app.Autogestion.models.login_model import loginModel, verificationModel

# Creación de token de acceso ---------------------------------------------------------------->
# Constantes de acceso
SECRET_KEY = config('SECRET_KEY')
ALGORITHM =  config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))

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

        if estado != "ACTIVO/A":
            return "Usuario Inactivo"

        result_write_list = await write_list(
            correo=correo,
            nombres=nombres,
            apellidos=apellidos,
            tipo_identificacion=Tipo_Identificacion,
            numero_identificacion=Identificacion,
            ingreso=ingreso
        )

        # Llama a send_verification_code_route con los datos necesarios
        verification_data = verificationModel(correo=correo)
        verification_result = await send_verification_code_route(verification_data)

        access_token_expires = ACCESS_TOKEN_EXPIRE_MINUTES
        login_token = create_access_token(data={"Tidentidad": Tipo_Identificacion, "Nidentidad": Identificacion,"Correo": correo,"WList":result_write_list,"VerificationCode":verification_result}, expires_delta=access_token_expires)

        return {"token": login_token}

        #return result_write_list, access_token, verification_result

""" descomentar para ver que esta enviando
        verification_data = verificationModel(correo=correo)
        print (correo)
        verification_result = await send_verification_code_route(verification_data)

        access_token_expires = ACCESS_TOKEN_EXPIRE_MINUTES
        access_token = create_access_token(data={"Tidentidad": Tipo_Identificacion, "Nidentidad": Identificacion}, expires_delta=access_token_expires)


        return result_write_list, access_token, verification_result """
