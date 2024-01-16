# -*- coding: utf-8 -*-
'''
Created on Mon Dec 19 2023

@author: Sebastian Suarez
'''

from fastapi import HTTPException, Header
import httpx
from jose import jwt
from app.Autogestion.controllers.history_controller import history_controller
from app.Autogestion.controllers.update_list_controller import uptade_ingreso
from app.Autogestion.models.history_model import historyModel
from app.Autogestion.models.update_list_model import UpdateListModel
from app.Autogestion.models.verification_model import VerificationModel
from app.Autogestion.models.login_model import verificationModel
from app.Autogestion.services.email_service import send_verification_code
from datetime import datetime, timedelta
from decouple import config
from app.Autogestion.services.token_User import create_access_token, get_user_current

from db.client_graph import get_access_token

# Creación de token de acceso ---------------------------------------------------------------->
# Constantes de acceso
SECRET_KEY = config('SECRET_KEY')
ALGORITHM =  config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))


# Environment variables
site = config('SITE_AGENDAMIENTO_ECOPETROL')
sub_site = config('SUBSITE_MEGAS_BULEVAR')
list_id = config('LIST_POBLACION')

# Almacenamiento en memoria para códigos de verificación (solo para ejemplo)
stored_verification_codes = {}

async def handle_unsuccessful_verification(item_id: str):
    # Función para manejar el caso de verificación no exitosa
    ingreso = "No Exitoso"
    update_data = UpdateListModel(item_id=item_id, ingreso=ingreso)
    await uptade_ingreso(update_data)
    raise HTTPException(status_code=400, detail="Código de verificación no encontrado")

async def send_verification_code_route(verification_data: verificationModel):
    # Ruta para enviar el código de verificación
    email = verification_data.correo
    verification_code = await send_verification_code(email)

    expiration_time = datetime.utcnow() + timedelta(minutes=5)

    stored_verification_codes[email] = {"code": verification_code, "expiration_time": expiration_time, "attempts": 0}

    return {"Código de verificación enviado"}
""" async def verify_code(
    verification_data: VerificationModel,
    authorization: str = Header(...),
):

    # Extraer el token del encabezado
    token = authorization.split(" ")[1]

    # Decodificar y validar el token
    token_decode = get_user_current(token)

    item_id = token_decode["WList"]["Registro"]

    # Ruta para verificar el código ingresado
    email = token_decode["Correo"]
    stored_code_data = stored_verification_codes.get(email, {})

    if not stored_code_data:
        # Manejar caso de código no encontrado
        await handle_unsuccessful_verification(item_id)

    expiration_time = stored_code_data.get("expiration_time", datetime.utcnow())

    if datetime.utcnow() > expiration_time:
        # Manejar caso de código expirado
        await handle_unsuccessful_verification(item_id)

    # Asegúrate de que el encabezado de autorización sea proporcionado y comienza con "Bearer"
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de autorización no válido")


    stored_code = stored_code_data.get("code", "")
    entered_code = verification_data.codigo

    if entered_code == stored_code:
        # Caso de verificación exitosa
        ingreso = "Exitoso"
        update_data = UpdateListModel(item_id=item_id, ingreso=ingreso)
        await uptade_ingreso(update_data)

        user_info = await get_user_info(token)


        # Llamada a history_controller
        history_result = await history_controller(token)


        # Configurar la expiración del token de acceso
        access_token_expires = ACCESS_TOKEN_EXPIRE_MINUTES

        # Crear un token de acceso con los datos necesarios
        Verify_token = create_access_token(data={
            "user_info": user_info
        }, expires_delta=access_token_expires)

        del stored_verification_codes[email]
        return {"mensaje": "Código verificado exitosamente", "token": Verify_token,
            "history_result": history_result}

    else:
        attempts = stored_code_data.get("attempts", 0)
        stored_verification_codes[email]["attempts"] = attempts + 1

        max_attempts = 3
        if attempts >= max_attempts:
            # Manejar caso de superar límite de intentos
            await handle_unsuccessful_verification(item_id)
            del stored_verification_codes[email]
            raise HTTPException(status_code=400, detail="Se ha superado el límite de intentos, por favor solicite un nuevo código.")
        else:
            # Manejar caso de código incorrecto
            raise HTTPException(status_code=400, detail="Código incorrecto, por favor inténtelo de nuevo.")

"""

async def verify_code(verification_data: VerificationModel):

    token = verification_data.token

    # Decodificar y validar el token
    token_decode = get_user_current(token)

    item_id = token_decode["WList"]["Registro"]

    email = token_decode["Correo"]
    stored_code_data = stored_verification_codes.get(email, {})

    if not stored_code_data:
        await handle_unsuccessful_verification(item_id)

    expiration_time = stored_code_data.get("expiration_time", datetime.utcnow())

    if datetime.utcnow() > expiration_time:
        await handle_unsuccessful_verification(item_id)

    stored_code = stored_code_data.get("code", "")
    entered_code = verification_data.codigo

    if entered_code == stored_code:
        ingreso = "Exitoso"
        update_data = UpdateListModel(item_id=item_id, ingreso=ingreso)
        await uptade_ingreso(update_data)

        user_info = await get_user_info(token)

        history_result = await history_controller(token)

        from fastapi import status

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        Verify_token = create_access_token(data={"user_info": user_info}, expires_delta=access_token_expires)

        del stored_verification_codes[email]
        return {"mensaje": "Código verificado exitosamente", "token": Verify_token, "history_result": history_result}

    else:
        attempts = stored_code_data.get("attempts", 0)
        stored_verification_codes[email]["attempts"] = attempts + 1

        max_attempts = 3
        if attempts >= max_attempts:
            await handle_unsuccessful_verification(item_id)
            del stored_verification_codes[email]
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Se ha superado el límite de intentos, por favor solicite un nuevo código.")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Código incorrecto, por favor inténtelo de nuevo.")

async def get_user_info(token: dict):
    try:
        token_db = await get_access_token()
        if token is None:
            raise HTTPException(
                status_code=401,
                detail="Token is missing",
                headers={"WWW-Authenticate": "Bearer"}
            )

        token_decode = get_user_current(token)

        tidentificacion = token_decode.get("Tidentidad")
        nidentificacion = token_decode.get("Nidentidad")
        correo = token_decode.get("Correo")

        URL = f'https://graph.microsoft.com/v1.0/sites/{site}/sites/{sub_site}/lists/{list_id}/items'
        headers = {"Authorization": f"Bearer {token_db}"}

        filter_query = {'$filter': f"fields/Title eq '{nidentificacion}' and fields/TipodeIdentificaci_x00f3_n eq '{tidentificacion}' and fields/E_x002d_mail eq '{correo}' ",
                        "$expand": "fields"}

        async with httpx.AsyncClient() as client:
            response = await client.get(URL, headers=headers, params=filter_query)
            response.raise_for_status()

        users = response.json()
        #return users

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error en la solicitud HTTP: {e}")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=response.status_code, detail=f"Error en la respuesta HTTP: {e}")

    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar JSON: {e}")
    # Response
    if users.get("value", []) == []:
        return "Usuario no encontrado"
    else:
        Identificacion = users["value"][0]["fields"]["Title"]
        Tipo_Identificacion = users["value"][0]["fields"]["TipodeIdentificaci_x00f3_n"]
        estado = users["value"][0]["fields"]["Estado"]
        nombres = users["value"][0]["fields"]["Nombres"]
        apellidos = users["value"][0]["fields"]["Apellidos"]
        telefono = users["value"][0]["fields"]["Celular"]
        Direccion = users["value"][0]["fields"].get("Direcci_x00f3_n", "No especificado")
        Tipo_Afiliacion = users["value"][0]["fields"].get("Descripci_x00f3_nFunci_x00f3_n_x", "No especificado")

    user_info = {
        "Nombre Completo": nombres + " " + apellidos,
        "Tidentidad": Tipo_Identificacion,
        "Nidentidad": Identificacion,
        "Correo": correo,
        "Telefono": telefono,
        "Estado": estado,
        "Direccion": Direccion,
        "Tipo_Afiliacion": Tipo_Afiliacion
    }

    return user_info