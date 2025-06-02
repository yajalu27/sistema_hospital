from abc import ABC, abstractmethod

class PacienteState(ABC):
    @abstractmethod
    def agregar_descargo(self, paciente, descargo_data):
        pass

    @abstractmethod
    def dar_alta(self, paciente):
        pass

    @abstractmethod
    def facturar(self, paciente, factura_data):
        pass

    @abstractmethod
    def get_estado(self):
        pass