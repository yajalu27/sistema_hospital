from fastapi import HTTPException, status
from app.repositories.servicio_repository import ServicioRepository
from app.schemas.servicio_producto_schema import ServicioResponse
from app.models.servicio import TipoServicio, Servicio

class ServicioService:
    def __init__(self, db):
        self.repository = ServicioRepository(db)

    def crear_servicio(self, servicio_data):
        return self.repository.crear_servicio(servicio_data)

    def obtener_servicio(self, servicio_id: int):
        servicio = self.repository.obtener_por_id(servicio_id)
        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no encontrado"
            )
        return servicio

    def listar_servicios(self, tipo: TipoServicio = None):
        if tipo:
            return self.repository.db.query(Servicio).filter(Servicio.tipo == tipo).all()
        return self.repository.listar_servicios()

    def actualizar_servicio(self, servicio_id: int, servicio_data):
        servicio = self.repository.actualizar_servicio(servicio_id, servicio_data.model_dump())
        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no encontrado"
            )
        return servicio

    def eliminar_servicio(self, servicio_id: int):
        if not self.repository.eliminar_servicio(servicio_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no encontrado"
            )
        return {"message": "Servicio eliminado correctamente"}