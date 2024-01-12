# Import Libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from decouple import config

# Import Routers
from app.Autogestion.routers import login_router
from app.Autogestion.routers import verification_router
from app.Autogestion.routers import update_list_router
from app.Autogestion.routers import history_router
from app.Autogestion.routers import space_available_router
from app.Autogestion.routers import cancellation_router
from app.Autogestion.routers import asignation_router
from app.Autogestion.routers import Prueba_Cookies_router


# SERVER
app = FastAPI()

# CORS
origins = ["*"
    #config("CLIENT_URL")
]

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Lista de orígenes permitidos
    allow_credentials=True,           # Permitir cookies / autorización con credenciales
    allow_methods=["*"],              # Permitir todos los métodos (GET, POST, PUT, etc.)
    allow_headers=["*"],              # Permitir todos los encabezados
)

# Routers
app.include_router(login_router.router)
app.include_router(verification_router.router)
app.include_router(update_list_router.router)
app.include_router(history_router.router)
app.include_router(space_available_router.router)
app.include_router(cancellation_router.router)
app.include_router(asignation_router.router)
app.include_router(Prueba_Cookies_router.router)

""" # Additional configuration
if __name__ == "__main__":
    import uvicorn

    # Get the configuration from environment variables or .env file
    host = config("HOST", default="127.0.0.1")
    port = config("PORT", default=8000, cast=int)

    # Run the application using uvicorn
    uvicorn.run(app, host=host, port=port)
"""