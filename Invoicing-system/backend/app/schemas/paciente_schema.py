from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class PacienteBase(BaseModel):
    nombre_completo: str = Field(..., example="Andres Rodriguez")
    afeccion: str = Field(..., example="Brazo roto")
    enfermedades: Optional[str] = Field(None, example="Ninguna")
    alergias: Optional[str] = Field(None, example="Ninguna")

class PacienteCreate(PacienteBase):
    pass

class PacienteResponse(PacienteBase):
    id: int
    fecha_ingreso: datetime
    estado: str

    class Config:
        from_attributes = True  # Habilita la conversión desde ORM

class LineaDescargoResponse(BaseModel):
    descripcion: str
    subtotal_sin_iva: float
    cantidad: int

class DescargoPacienteResponse(BaseModel):
    id: int
    fecha: datetime
    total: float
    lineas: List[LineaDescargoResponse] = []

class PacienteConDescargosSimpleResponse(BaseModel):
    id: int
    nombre_completo: str
    descargos: List[DescargoPacienteResponse] = []
    
    class Config:
        from_attributes = True

class PacienteConDescargosResponse(BaseModel):
    id: int
    nombre_completo: str
    descargos: List[DescargoPacienteResponse] = []
    afeccion: Optional[str] = None
    fecha_ingreso: Optional[datetime] = None
    estado: Optional[str] = None
    
    class Config:
        from_attributes = True