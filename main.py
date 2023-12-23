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

# SERVER
app = FastAPI()

# CORS
origins = [
    config("CLIENT_URL")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"]
)

# Routers
app.include_router(login_router.router)
app.include_router(verification_router.router)
app.include_router(update_list_router.router)
app.include_router(history_router.router)
app.include_router(space_available_router.router)
app.include_router(cancellation_router.router)
# Additional configuration
if __name__ == "__main__":
    import uvicorn

    # Get the configuration from environment variables or .env file
    host = config("HOST", default="127.0.0.1")
    port = config("PORT", default=8000, cast=int)

    # Run the application using uvicorn
    uvicorn.run(app, host=host, port=port)
