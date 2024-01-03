from pydantic import BaseModel

class AsignationModel(BaseModel):
    Id: int
    modalidad: str
    nombre: str


class checkAvailabilityModel(BaseModel):
    id_registro: int
