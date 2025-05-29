from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Descargo(Base):
    __tablename__ = "descargos"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    fecha = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, default=0.0, nullable=False)
    
    # Relaciones
    paciente = relationship("Paciente", back_populates="descargos")
    lineas_transaccionales = relationship(
        "LineaDocumentoTransaccional", 
        back_populates="descargo",
        cascade="all, delete-orphan",
        lazy="joined"
    )
    
    @property
    def lineas(self):
        if not hasattr(self, '_lineas'):
            self._lineas = []
            for linea_trans in self.lineas_transaccionales:
                if linea_trans.linea_descargo:
                    self._lineas.append({
                        "id": linea_trans.linea_descargo.id,
                        "descripcion": linea_trans.linea_descargo.descripcion,
                        "subtotal_sin_iva": linea_trans.linea_descargo.subtotal_sin_iva,
                        "cantidad": linea_trans.cantidad,
                        "servicio_id": linea_trans.servicio_id,
                        "producto_id": linea_trans.producto_id
                    })
        return self._lineas
    
    @lineas.setter
    def lineas(self, value):
        self._lineas = value