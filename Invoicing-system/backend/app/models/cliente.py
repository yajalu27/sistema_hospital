from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200))
    telefono = Column(String(20))
    correo = Column(String(100))
    
    facturas = relationship("Factura", back_populates="cliente")