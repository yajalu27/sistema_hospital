from abc import ABC, abstractmethod
from app.models.servicio import Servicio, TipoServicio
from app.schemas.servicio_producto_schema import ServicioCreate

class ServicioFactory(ABC):
    """Interfaz para la fábrica de servicios."""
    @abstractmethod
    def create_servicio(self, servicio_data: ServicioCreate) -> Servicio:
        pass

class AtencionMedicaFactory(ServicioFactory):
    """Fábrica para servicios de atención médica."""
    def create_servicio(self, servicio_data: ServicioCreate) -> Servicio:
        servicio = Servicio(
            tipo=TipoServicio.atencion_medica,
            precio_base=servicio_data.precio_base,
            descripcion=servicio_data.descripcion or "Consulta médica general"
        )
        return servicio

class ExamenLaboratorioFactory(ServicioFactory):
    """Fábrica para exámenes de laboratorio."""
    def create_servicio(self, servicio_data: ServicioCreate) -> Servicio:
        servicio = Servicio(
            tipo=TipoServicio.examen_laboratorio,
            precio_base=servicio_data.precio_base * 1.1,  # 10% adicional por costos de laboratorio
            descripcion=servicio_data.descripcion or "Examen de laboratorio estándar"
        )
        return servicio

class SuministroMedicamentoFactory(ServicioFactory):
    """Fábrica para suministro de medicamentos."""
    def create_servicio(self, servicio_data: ServicioCreate) -> Servicio:
        servicio = Servicio(
            tipo=TipoServicio.suministro_medicamento,
            precio_base=servicio_data.precio_base,
            descripcion=servicio_data.descripcion or "Suministro de medicamentos"
        )
        return servicio

class ProcedimientoMedicoFactory(ServicioFactory):
    """Fábrica para procedimientos médicos."""
    def create_servicio(self, servicio_data: ServicioCreate) -> Servicio:
        servicio = Servicio(
            tipo=TipoServicio.procedimiento_medico,
            precio_base=servicio_data.precio_base * 1.2,  # 20% adicional por complejidad
            descripcion=servicio_data.descripcion or "Procedimiento médico especializado"
        )
        return servicio

class ImagenRayosXFactory(ServicioFactory):
    """Fábrica para imágenes de rayos X."""
    def create_servicio(self, servicio_data: ServicioCreate) -> Servicio:
        servicio = Servicio(
            tipo=TipoServicio.imagen_rayos_x,
            precio_base=servicio_data.precio_base * 1.15,  #15% adicional por equipo
            descripcion=servicio_data.descripcion or "Imagen de rayos X"
        )
        return servicio

class ServicioFactoryManager:
    """Gestor de fábricas de servicios."""
    @staticmethod
    def get_factory(tipo: TipoServicio) -> ServicioFactory:
        factories = {
            TipoServicio.atencion_medica: AtencionMedicaFactory(),
            TipoServicio.examen_laboratorio: ExamenLaboratorioFactory(),
            TipoServicio.suministro_medicamento: SuministroMedicamentoFactory(),
            TipoServicio.procedimiento_medico: ProcedimientoMedicoFactory(),
            TipoServicio.imagen_rayos_x: ImagenRayosXFactory()
        }
        factory = factories.get(tipo)
        if not factory:
            raise ValueError(f"Tipo de servicio no soportado: {tipo}")
        return factory