from sqlalchemy.orm import Session
from app.models.producto import Producto, TipoProducto
from app.schemas.servicio_producto_schema import ProductoCreate
from app.services.factories.product_factory import ProductoFactoryManager

class ProductoRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear_producto(self, producto: ProductoCreate):
        # Obtener la fábrica según el tipo de producto
        factory = ProductoFactoryManager.get_factory(producto.tipo)
        # Crear la instancia del producto usando la fábrica
        db_producto = factory.create_producto(producto)
        self.db.add(db_producto)
        self.db.commit()
        self.db.refresh(db_producto)
        return db_producto

    def obtener_por_id(self, producto_id: int):
        return self.db.query(Producto).filter(Producto.id == producto_id).first()

    def listar_productos(self):
        return self.db.query(Producto).all()

    def actualizar_producto(self, producto_id: int, producto_data: dict):
        producto = self.obtener_por_id(producto_id)
        if producto:
            for key, value in producto_data.items():
                setattr(producto, key, value)
            self.db.commit()
            self.db.refresh(producto)
        return producto

    def eliminar_producto(self, producto_id: int):
        producto = self.obtener_por_id(producto_id)
        if producto:
            self.db.delete(producto)
            self.db.commit()
        return producto