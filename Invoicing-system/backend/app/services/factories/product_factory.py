from abc import ABC, abstractmethod
from app.models.producto import Producto, TipoProducto
from app.schemas.servicio_producto_schema import ProductoCreate

class ProductoFactory(ABC):
    """Interfaz para la fábrica de productos."""
    @abstractmethod
    def create_producto(self, producto_data: ProductoCreate) -> Producto:
        pass

class MedicamentosFactory(ProductoFactory):
    """Fábrica para productos de tipo medicamentos."""
    def create_producto(self, producto_data: ProductoCreate) -> Producto:
        producto = Producto(
            tipo=TipoProducto.medicamentos,
            precio_base=producto_data.precio_base * 1.05,  # 5% adicional por costos de regulación
            descripcion=producto_data.descripcion or "Medicamento genérico"
        )
        return producto

class InsumosMedicosFactory(ProductoFactory):
    """Fábrica para productos de tipo insumos médicos."""
    def create_producto(self, producto_data: ProductoCreate) -> Producto:
        producto = Producto(
            tipo=TipoProducto.insumos_medicos,
            precio_base=producto_data.precio_base * 1.1,  # 10% adicional por costos de importación
            descripcion=producto_data.descripcion or "Insumo médico estándar"
        )
        return producto

class SuplementosNutricionalesFactory(ProductoFactory):
    """Fábrica para productos de tipo suplementos nutricionales."""
    def create_producto(self, producto_data: ProductoCreate) -> Producto:
        producto = Producto(
            tipo=TipoProducto.suplementos_nutricionales,
            precio_base=producto_data.precio_base,
            descripcion=producto_data.descripcion or "Suplemento nutricional estándar"
        )
        return producto

class VacunasFactory(ProductoFactory):
    """Fábrica para productos de tipo vacunas."""
    def create_producto(self, producto_data: ProductoCreate) -> Producto:
        producto = Producto(
            tipo=TipoProducto.vacunas,
            precio_base=producto_data.precio_base * 1.15,  # 15% adicional por costos de almacenamiento en frío
            descripcion=producto_data.descripcion or "Vacuna estándar"
        )
        return producto

class ProductoFactoryManager:
    """Gestor de fábricas de productos."""
    @staticmethod
    def get_factory(tipo: TipoProducto) -> ProductoFactory:
        factories = {
            TipoProducto.medicamentos: MedicamentosFactory(),
            TipoProducto.insumos_medicos: InsumosMedicosFactory(),
            TipoProducto.suplementos_nutricionales: SuplementosNutricionalesFactory(),
            TipoProducto.vacunas: VacunasFactory()
        }
        factory = factories.get(tipo)
        if not factory:
            raise ValueError(f"Tipo de producto no soportado: {tipo}")
        return factory