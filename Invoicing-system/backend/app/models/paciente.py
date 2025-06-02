from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.services.states.paciente_states import InternadoState, AltaState, FacturadoState
from sqlalchemy import event

class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(100), nullable=False)
    fecha_ingreso = Column(DateTime, default=datetime.utcnow)
    fecha_alta = Column(DateTime, nullable=True)
    afeccion = Column(String(200))
    enfermedades = Column(String(200))
    alergias = Column(String(200))
    estado = Column(String(20), default="internado")  # internado/alta/facturado
    
    descargos = relationship("Descargo", back_populates="paciente")
    facturas = relationship("Factura", back_populates="paciente")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, '_state'):
            self._state = InternadoState()

    def agregar_descargo(self, descargo_data):
        """Delegar la acción al estado actual."""
        return self._state.agregar_descargo(self, descargo_data)

    def dar_alta(self):
        """Delegar la acción al estado actual."""
        return self._state.dar_alta(self)

    def facturar(self, factura_data):
        """Delegar la acción al estado actual."""
        return self._state.facturar(self, factura_data)

    def get_estado(self):
        """Obtener el estado actual desde la base de datos."""
        # Sincronizar _state con el valor de estado en la base de datos
        if self.estado == "internado":
            self._state = InternadoState()
        elif self.estado == "alta":
            self._state = AltaState()
        elif self.estado == "facturado":
            self._state = FacturadoState()
        return self.estado  # Devolver el valor de la columna estado

    def esta_facturado(self):
        """Verificar si el paciente está facturado."""
        return self.get_estado() == "facturado"

# Evento para inicializar el estado al cargar desde la base de datos
@event.listens_for(Paciente, "load")
def receive_load(paciente, _):
    if not hasattr(paciente, '_state'):
        if paciente.estado == "internado":
            paciente._state = InternadoState()
        elif paciente.estado == "alta":
            paciente._state = AltaState()
        elif paciente.estado == "facturado":
            paciente._state = FacturadoState()