from fastapi import HTTPException, status
from app.repositories.producto_repository import ProductoRepository
from app.schemas.servicio_producto_schema import ProductoResponse

class ProductoService:
    def __init__(self, db):
        self.repository = ProductoRepository(db)

    def crear_producto(self, producto_data):
        return self.repository.crear_producto(producto_data)

    def obtener_producto(self, producto_id: int):
        producto = self.repository.obtener_por_id(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        return producto

    def listar_productos(self):
        return self.repository.listar_productos()

    def actualizar_producto(self, producto_id: int, producto_data):
        producto = self.repository.actualizar_producto(producto_id, producto_data.model_dump())
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        return producto

    def eliminar_producto(self, producto_id: int):
        if not self.repository.eliminar_producto(producto_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        return {"message": "Producto eliminado correctamente"}