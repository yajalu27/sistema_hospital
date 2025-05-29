from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional, List

class FechaBase(BaseModel):
    fecha_emision: Optional[date] = None
    fecha_actualizacion: Optional[date] = None

class IdentificacionBase(BaseModel):
    identificacion: str
    telefono: Optional[str] = None
    correo: Optional[str] = None