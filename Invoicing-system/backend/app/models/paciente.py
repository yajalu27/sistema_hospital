from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(100), nullable=False)
    fecha_ingreso = Column(DateTime, default=datetime.utcnow)
    fecha_alta = Column(DateTime, nullable=True)
    afeccion = Column(String(200))
    enfermedades = Column(String(200))
    alergias = Column(String(200))
    estado = Column(String(20), default="internado")  # internado/alta
    
    descargos = relationship("Descargo", back_populates="paciente")
    facturas = relationship("Factura", back_populates="paciente")

    def set_alta(self):
        self.estado = "alta"
        self.fecha_alta = datetime.utcnow()

    def esta_facturado(self):
        return len(self.facturas) > 0