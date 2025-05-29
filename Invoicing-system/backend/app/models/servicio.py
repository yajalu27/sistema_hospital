from sqlalchemy import Column, Integer, String, Float, Enum
from app.core.database import Base
from enum import Enum as PyEnum

class TipoServicio(str, PyEnum):
    atencion_medica = "atencion_medica"
    examen_laboratorio = "examen_laboratorio"
    suministro_medicamento = "suministro_medicamento"
    procedimiento_medico = "procedimiento_medico"

class Servicio(Base):
    __tablename__ = "servicios"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoServicio))
    precio_base = Column(Float)
    descripcion = Column(String(200))