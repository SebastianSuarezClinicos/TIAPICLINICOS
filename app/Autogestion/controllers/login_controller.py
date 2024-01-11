# imports libraries
from fastapi import HTTPException
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
ACCESS_TOKEN_EXPIRE_MINUTES = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))

# Environment variables
site = config('SITE_AGENDAMIENTO_ECOPETROL')
sub_site = config('SUBSITE_MEGAS_BULEVAR')
list_id = config('LIST_POBLACION')

# CONTROLADOR
async def login_controller(login: loginModel):
    try:
        # Obtener el token de acceso para operaciones en la base de datos
        token = await get_access_token()

        # Extrayendo parámetros de inicio de sesión de la solicitud
        tidentificacion = login.tipodeidentificacion
        nidentificacion = login.numerodeidentificacion
        correo = login.correo

        # Configuración de la URL para la API de Microsoft Graph
        URL = f'https://graph.microsoft.com/v1.0/sites/{site}/sites/{sub_site}/lists/{list_id}/items'
        headers = {"Authorization": f"Bearer {token}"}

        # Preparando la consulta de filtro para la solicitud a la API
        filter_query = {'$filter': f"fields/Title eq '{nidentificacion}' and fields/TipodeIdentificaci_x00f3_n eq '{tidentificacion}' and fields/E_x002d_mail eq '{correo}' ",
                        "$expand": "fields"}

        # Solicitud HTTP
        async with httpx.AsyncClient() as client:
            response = await client.get(URL, headers=headers, params=filter_query)
            response.raise_for_status
            users = response.json()

    # Capturar excepciones durante la ejecución
    except httpx.RequestError as e:
        raise HTTPException(status_code=500,
                            detail=f"Error en la solicitud HTTP: {e}")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=response.status_code,
                            detail=f"Error en la respuesta HTTP: {e}")

    except ValueError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al analizar JSON: {e}")

    # Manejar la respuesta
    if users.get("value", []) == []:
        return "Usuario no encontrado"
    else:
        Identificacion = users["value"][0]["fields"]["Title"]
        Tipo_Identificacion = users["value"][0]["fields"]["TipodeIdentificaci_x00f3_n"]
        estado = users["value"][0]["fields"]["Estado"]
        nombres = users["value"][0]["fields"]["Nombres"]
        apellidos = users["value"][0]["fields"]["Apellidos"]
        ingreso = "Pendiente"

        if estado != "Activo":
            return "Usuario Inactivo"

        # Realizar operaciones de escritura en la lista
        result_write_list = await write_list(
            correo=correo,
            nombres=nombres,
            apellidos=apellidos,
            tipo_identificacion=Tipo_Identificacion,
            numero_identificacion=Identificacion,
            ingreso=ingreso
        )

        # Llamar a la ruta de envío de código de verificación con los datos necesarios
        verification_data = verificationModel(correo=correo)
        verification_result = await send_verification_code_route(verification_data)

        # Configurar la expiración del token de acceso
        access_token_expires = ACCESS_TOKEN_EXPIRE_MINUTES

        # Crear un token de acceso con los datos necesarios
        login_info = create_access_token(data={
            "Tidentidad": Tipo_Identificacion,
            "Nidentidad": Identificacion,
            "Correo": correo,
            "WList": result_write_list,
            "VerificationCode": verification_result
        }, expires_delta=access_token_expires)

        return login_info

        #return result_write_list, access_token, verification_result

""" descomentar para ver que esta enviando
        verification_data = verificationModel(correo=correo)
        print (correo)
        verification_result = await send_verification_code_route(verification_data)

        access_token_expires = ACCESS_TOKEN_EXPIRE_MINUTES
        access_token = create_access_token(data={"Tidentidad": Tipo_Identificacion, "Nidentidad": Identificacion}, expires_delta=access_token_expires)


        return result_write_list, access_token, verification_result """
