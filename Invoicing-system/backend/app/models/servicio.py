from sqlalchemy.ext.declarative import DeclarativeMeta
from abc import ABCMeta, abstractmethod

# Define una metaclass que combine DeclarativeMeta y ABCMeta
class HybridMeta(DeclarativeMeta, ABCMeta):
    pass

# Interfaz para los productos (vehículos)
class ServicioInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_descripcion(self) -> str:
        """Método abstracto para obtener la descripción del servicio."""
        pass

    @abstractmethod
    def calcular_precio(self) -> float:
        """Método abstracto para calcular el precio del servicio."""
        pass

from sqlalchemy import Column, Integer, String, Float, Enum
from app.core.database import Base
from enum import Enum as PyEnum

class TipoServicio(str, PyEnum):
    atencion_medica = "atencion_medica"
    examen_laboratorio = "examen_laboratorio"
    suministro_medicamento = "suministro_medicamento"
    procedimiento_medico = "procedimiento_medico"
    imagen_rayos_x = "imagen_rayos_x"

class Servicio(Base, ServicioInterface, metaclass=HybridMeta):
    __tablename__ = "servicios"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoServicio))
    precio_base = Column(Float)
    descripcion = Column(String(200))

    def get_descripcion(self) -> str:
        """Devuelve la descripción del servicio."""
        return f"Servicio de {self.tipo}: {self.descripcion}"

    def calcular_precio(self) -> float:
        """Calcula el precio base del servicio (puede ser sobrescrito por fábricas específicas)."""
        return self.precio_base