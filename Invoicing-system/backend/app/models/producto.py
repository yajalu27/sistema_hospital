from sqlalchemy.ext.declarative import DeclarativeMeta
from abc import ABCMeta, abstractmethod
from sqlalchemy import Column, Integer, String, Float, Enum
from app.core.database import Base
from enum import Enum as PyEnum

# Define una metaclass que combine DeclarativeMeta y ABCMeta
class HybridMeta(DeclarativeMeta, ABCMeta):
    pass

class TipoProducto(str, PyEnum):
    medicamentos = "medicamentos"
    insumos_medicos = "insumos_medicos"
    suplementos_nutricionales = "suplementos_nutricionales"
    vacunas = "vacunas"

class ProductoInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_descripcion(self) -> str:
        """Método abstracto para obtener la descripción del producto."""
        pass

    @abstractmethod
    def calcular_precio(self) -> float:
        """Método abstracto para calcular el precio del producto."""
        pass

class Producto(Base, ProductoInterface, metaclass=HybridMeta):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoProducto))
    precio_base = Column(Float)
    descripcion = Column(String(200))

    def get_descripcion(self) -> str:
        """Devuelve la descripción del producto."""
        return f"Producto de tipo {self.tipo}: {self.descripcion}"

    def calcular_precio(self) -> float:
        """Calcula el precio base del producto (puede ser sobrescrito por fábricas específicas)."""
        return self.precio_base