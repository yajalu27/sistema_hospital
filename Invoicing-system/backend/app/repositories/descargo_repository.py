from sqlalchemy.orm import Session
from app.models import Descargo, LineaDocumentoTransaccional, LineaDescargo, Servicio, Producto
from app.schemas.descargo_schema import LineaDescargoCreate
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from app.services.prototypes.prototype_base import (
    linea_transaccional_prototype_servicio,
    linea_transaccional_prototype_producto,
    linea_descargo_prototype
)

class DescargoRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear_descargo_con_lineas(self, paciente_id: int, lineas: list[LineaDescargoCreate]):
        try:
            descargo = Descargo(paciente_id=paciente_id)
            self.db.add(descargo)
            self.db.commit()
            self.db.refresh(descargo)
            
            total = 0.0
            lineas_response = []
            
            for linea in lineas:
                if linea.servicio_id is not None and linea.producto_id is not None:
                    raise HTTPException(
                        status_code=400,
                        detail="Cada línea debe tener solo servicio o producto, no ambos"
                    )
                
                # Seleccionar prototipo adecuado
                linea_trans_prototype = (
                    linea_transaccional_prototype_servicio.clone() if linea.servicio_id
                    else linea_transaccional_prototype_producto.clone() if linea.producto_id
                    else linea_transaccional_prototype_servicio.clone()
                )
                
                precio = self._obtener_precio(linea.servicio_id, linea.producto_id)
                subtotal = precio * linea.cantidad
                total += subtotal
                
                # Personalizar el prototipo
                linea_trans = linea_trans_prototype
                linea_trans.cantidad = linea.cantidad
                linea_trans.servicio_id = linea.servicio_id
                linea_trans.producto_id = linea.producto_id
                linea_trans.descargo_id = descargo.id
                
                self.db.add(linea_trans)
                self.db.commit()
                
                # Clonar y personalizar LineaDescargo
                linea_descargo = linea_descargo_prototype.clone()
                descripcion = self._generar_descripcion(linea.servicio_id, linea.producto_id)
                linea_descargo.descripcion = descripcion
                linea_descargo.subtotal_sin_iva = subtotal
                linea_descargo.linea_transaccional_id = linea_trans.id
                
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
            return servicio.calcular_precio()
        elif producto_id:
            producto = self.db.query(Producto).filter(Producto.id == producto_id).first()
            if not producto:
                raise HTTPException(
                    status_code=404,
                    detail=f"Producto con ID {producto_id} no encontrado"
                )
            return producto.calcular_precio()
        else:
            raise HTTPException(
                status_code=400,
                detail="Se requiere servicio_id o producto_id"
            )

    def _generar_descripcion(self, servicio_id: int = None, producto_id: int = None) -> str:
        if servicio_id:
            servicio = self.db.query(Servicio).filter(Servicio.id == servicio_id).first()
            return f"Servicio: {servicio.get_descripcion()}" if servicio else f"Servicio ID: {servicio_id}"
        elif producto_id:
            producto = self.db.query(Producto).filter(Producto.id == producto_id).first()
            return f"Producto: {producto.get_descripcion()}" if producto else f"Producto ID: {producto_id}"
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