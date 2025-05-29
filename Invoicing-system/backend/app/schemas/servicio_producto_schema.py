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
    comida = "comida"
    vacunas = "vacunas"
    medicamentos = "medicamentos"
    insumos_medicos = "insumos_medicos"

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