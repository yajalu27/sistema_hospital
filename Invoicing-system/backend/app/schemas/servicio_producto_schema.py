from enum import Enum
from pydantic import BaseModel
from typing import Optional

# Enums para validación
class TipoServicioEnum(str, Enum):
    atencion_medica = "atencion_medica"
    examen_laboratorio = "examen_laboratorio"
    suministro_medicamento = "suministro_medicamento"
    procedimiento_medico = "procedimiento_medico"

class TipoProductoEnum(str, Enum):
    medicamentos = "medicamentos"
    insumos_medicos = "insumos_medicos"
    suplementos_nutricionales = "suplementos_nutricionales"
    vacunas = "vacunas"

# Esquemas para Servicios
class ServicioBase(BaseModel):
    tipo: TipoServicioEnum
    precio_base: float
    descripcion: str

class ServicioCreate(ServicioBase):
    pass

class ServicioResponse(ServicioBase):
    id: int
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {"id": 1, "tipo": "atencion_medica", "precio_base": 100.0, "descripcion": "Consulta general"}
        }

# Esquemas para Productos
class ProductoBase(BaseModel):
    tipo: TipoProductoEnum
    precio_base: float
    descripcion: str

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {"id": 1, "tipo": "medicamentos", "precio_base": 50.0, "descripcion": "Paracetamol 500mg"}
        }