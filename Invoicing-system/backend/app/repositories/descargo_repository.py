from sqlalchemy.orm import Session
from app.models import Descargo, LineaDocumentoTransaccional, LineaDescargo, Servicio, Producto
from app.schemas.descargo_schema import LineaDescargoCreate
from fastapi import HTTPException
from sqlalchemy.orm import joinedload

class DescargoRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear_descargo_con_lineas(self, paciente_id: int, lineas: list[LineaDescargoCreate]):
        try:
            descargo = Descargo(paciente_id=paciente_id)
            self.db.add(descargo)
            self.db.commit()
            self.db.refresh(descargo)
            a
            total = 0.0
            lineas_response = []
            
            for linea in lineas:
                if linea.servicio_id is not None and linea.producto_id is not None:
                    raise HTTPException(
                        status_code=400,
                        detail="Cada línea debe tener solo servicio o producto, no ambos"
                    )
                
                precio = self._obtener_precio(linea.servicio_id, linea.producto_id)
                subtotal = precio * linea.cantidad
                total += subtotal
                
                linea_trans = LineaDocumentoTransaccional(
                    descargo_id=descargo.id,
                    servicio_id=linea.servicio_id,
                    producto_id=linea.producto_id,
                    cantidad=linea.cantidad
                )
                self.db.add(linea_trans)
                self.db.commit()
                
                descripcion = self._generar_descripcion(linea.servicio_id, linea.producto_id)
                linea_descargo = LineaDescargo(
                    linea_transaccional_id=linea_trans.id,
                    descripcion=descripcion,
                    subtotal_sin_iva=subtotal
                )
                self.db.add(linea_descargo)
                self.db.commit()
                
                lineas_response.append({
                    "id": linea_descargo.id,
                    "descripcion": descripcion,
                    "subtotal_sin_iva": subtotal,
                    "cantidad": linea.cantidad,
                    "servicio_id": linea.servicio_id,
                    "producto_id": linea.producto_id
                })
            
            descargo.total = total
            self.db.commit()
            self.db.refresh(descargo)
            
            setattr(descargo, 'lineas', lineas_response)
            return descargo
            
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear descargo: {str(e)}"
            )

    def _obtener_precio(self, servicio_id: int = None, producto_id: int = None) -> float:
        if servicio_id:
            servicio = self.db.query(Servicio).filter(Servicio.id == servicio_id).first()
            if not servicio:
                raise HTTPException(
                    status_code=404,
                    detail=f"Servicio con ID {servicio_id} no encontrado"
                )
            return servicio.precio_base
        elif producto_id:
            producto = self.db.query(Producto).filter(Producto.id == producto_id).first()
            if not producto:
                raise HTTPException(
                    status_code=404,
                    detail=f"Producto con ID {producto_id} no encontrado"
                )
            return producto.precio_base
        else:
            raise HTTPException(
                status_code=400,
                detail="Se requiere servicio_id o producto_id"
            )

    def _generar_descripcion(self, servicio_id: int = None, producto_id: int = None) -> str:
        if servicio_id:
            servicio = self.db.query(Servicio).filter(Servicio.id == servicio_id).first()
            return f"Servicio: {servicio.descripcion}" if servicio else f"Servicio ID: {servicio_id}"
        elif producto_id:
            producto = self.db.query(Producto).filter(Producto.id == producto_id).first()
            return f"Producto: {producto.descripcion}" if producto else f"Producto ID: {producto_id}"
        return "Ítem no especificado"
    
    def obtener_descargos_por_paciente(self, paciente_id: int):
        descargos = self.db.query(Descargo)\
            .filter(Descargo.paciente_id == paciente_id)\
            .options(
                joinedload(Descargo.lineas_transaccionales)
                .joinedload(LineaDocumentoTransaccional.linea_descargo)
            )\
            .all()
        return descargos