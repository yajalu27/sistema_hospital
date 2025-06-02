from app.services.states.paciente_state import PacienteState
from app.models.descargo import Descargo
from app.models.linea_transaccional import Factura
from datetime import datetime

class InternadoState(PacienteState):
    def agregar_descargo(self, paciente, descargo_data):
        """Permite agregar descargos mientras el paciente está internado."""
        descargo = Descargo(paciente_id=paciente.id, **descargo_data)
        paciente.descargos.append(descargo)  # Agregar a la relación
        return descargo

    def dar_alta(self, paciente):
        """Cambia el estado a AltaState."""
        paciente.estado = "alta"
        paciente.fecha_alta = datetime.utcnow()
        paciente._state = AltaState()
        return True

    def facturar(self, paciente, factura_data):
        """No permite facturar mientras el paciente está internado."""
        raise ValueError("No se puede facturar a un paciente internado.")

    def get_estado(self):
        return "internado"

class AltaState(PacienteState):
    def agregar_descargo(self, paciente, descargo_data):
        """No permite agregar descargos después de dar de alta."""
        raise ValueError("No se pueden agregar descargos a un paciente dado de alta.")

    def dar_alta(self, paciente):
        """El paciente ya está dado de alta, no se permite repetir esta acción."""
        raise ValueError("El paciente ya está dado de alta.")

    def facturar(self, paciente, factura_data):
        """Cambia el estado a FacturadoState y genera la factura si se asocia correctamente."""
        factura = Factura(**factura_data)
        paciente.facturas.append(factura)  # Agregar a la relación
        # Verificar si la factura se asoció correctamente
        if factura in paciente.facturas:
            paciente.estado = "facturado"  # Actualizar el estado solo si la factura está asociada
            paciente._state = FacturadoState()
            print(f"Factura asociada exitosamente. Estado: {paciente.estado}, _state: {paciente._state.get_estado()}")
        else:
            print("Error: La factura no se asoció correctamente al paciente.")
        return factura

    def get_estado(self):
        return "alta"

class FacturadoState(PacienteState):
    def agregar_descargo(self, paciente, descargo_data):
        """No permite agregar descargos después de facturar."""
        raise ValueError("No se pueden agregar descargos a un paciente facturado.")

    def dar_alta(self, paciente):
        """No permite cambiar el alta después de facturar."""
        raise ValueError("El paciente ya está facturado, no se puede dar de alta nuevamente.")

    def facturar(self, paciente, factura_data):
        """No permite facturar nuevamente."""
        raise ValueError("El paciente ya está facturado.")

    def get_estado(self):
        return "facturado"