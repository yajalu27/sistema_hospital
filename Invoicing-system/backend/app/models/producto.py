from sqlalchemy import Column, Integer, String, Float, Enum
from app.core.database import Base
from enum import Enum as PyEnum

class TipoProducto(str, PyEnum):
    comida = "comida"
    vacunas = "vacunas"
    medicamentos = "medicamentos"
    insumos_medicos = "insumos_medicos"

class Producto(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoProducto))
    precio_base = Column(Float)
    descripcion = Column(String(200))