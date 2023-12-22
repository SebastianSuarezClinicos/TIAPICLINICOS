

# Import libraries
from pydantic import BaseModel


# Classes
class historyModel(BaseModel):
    tipodeidentificacion: str
    numerodeidentificacion: str