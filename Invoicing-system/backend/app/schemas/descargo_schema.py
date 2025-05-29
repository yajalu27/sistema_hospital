from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum
from app.schemas.paciente_schema import PacienteResponse

class LineaDescargoCreate(BaseModel):
    servicio_id: Optional[int] = Field(None, description="ID del servicio (opcional)")
    producto_id: Optional[int] = Field(None, description="ID del producto (opcional)")
    cantidad: int = Field(1, gt=0, description="Cantidad debe ser mayor a 0")

    @validator('*', pre=True)
    def check_servicio_or_producto(cls, v, values, **kwargs):
        if 'servicio_id' in values and 'producto_id' in values:
            if values['servicio_id'] is not None and values['producto_id'] is not None:
                raise ValueError("Solo se permite servicio O producto, no ambos")
        return v

class DescargoCreate(BaseModel):
    paciente_id: int
    lineas: List[LineaDescargoCreate] = Field(..., min_items=1)

class LineaDescargoResponse(BaseModel):
    id: int
    descripcion: str
    subtotal_sin_iva: float = 0.0
    cantidad: int
    servicio_id: Optional[int] = None
    producto_id: Optional[int] = None

class DescargoResponse(BaseModel):
    id: int
    paciente_id: int
    fecha: datetime
    total: float = 0.0
    lineas: List[LineaDescargoResponse] = []
    
    class Config:
        from_attributes = True

class PacienteConDescargosSimpleResponse(PacienteResponse):
    descargos: List[DescargoResponse] = []
    
    class Config:
        from_attributes = True