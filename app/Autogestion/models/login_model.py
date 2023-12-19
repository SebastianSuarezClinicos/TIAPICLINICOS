

# Import libraries
from pydantic import BaseModel


# Classes
class loginModel(BaseModel):
  tipodeidentificacion: str
  numerodeidentificacion: str
  correo: str

class verificationModel(BaseModel):
  correo: str

