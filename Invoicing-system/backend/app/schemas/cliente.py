from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str
    direccion: str
    telefono: str
    correo: str

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None

class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True  # Compatible con Pydantic v2