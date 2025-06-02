from sqlalchemy.orm import Session
from app.models.servicio import Servicio, TipoServicio
from app.schemas.servicio_producto_schema import ServicioCreate
from app.services.factories.service_factory import ServicioFactoryManager

class ServicioRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear_servicio(self, servicio: ServicioCreate):
        # Obtener la fábrica según el tipo de servicio
        factory = ServicioFactoryManager.get_factory(servicio.tipo)
        # Crear la instancia del servicio usando la fábrica
        db_servicio = factory.create_servicio(servicio)
        self.db.add(db_servicio)
        self.db.commit()
        self.db.refresh(db_servicio)
        return db_servicio

    def obtener_por_id(self, servicio_id: int):
        return self.db.query(Servicio).filter(Servicio.id == servicio_id).first()

    def listar_servicios(self):
        return self.db.query(Servicio).all()

    def actualizar_servicio(self, servicio_id: int, servicio_data: dict):
        servicio = self.obtener_por_id(servicio_id)
        if servicio:
            for key, value in servicio_data.items():
                setattr(servicio, key, value)
            self.db.commit()
            self.db.refresh(servicio)
        return servicio

    def eliminar_servicio(self, servicio_id: int):
        servicio = self.obtener_por_id(servicio_id)
        if servicio:
            self.db.delete(servicio)
            self.db.commit()
        return servicio