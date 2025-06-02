from sqlalchemy.orm import Session, joinedload
from app.models import Factura, LineaFactura, LineaDocumentoTransaccional
from app.services.prototypes.prototype_base import linea_factura_prototype

class FacturaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_factura(self, factura_data, lineas_data):
        factura = Factura(**factura_data)
        self.db.add(factura)
        self.db.commit()
        self.db.refresh(factura)

        for linea_data in lineas_data:
            # Clonacion de la linea factura
            linea_factura = linea_factura_prototype.clone()
            linea_factura.iva = linea_data.get("iva", 0.16)
            linea_factura.total_con_iva = linea_data.get("total_con_iva", 0.0)
            linea_factura.linea_transaccional_id = linea_data.get("linea_transaccional_id")
            linea_factura.factura_id = factura.id
            
            self.db.add(linea_factura)

        self.db.commit()
        return factura

    def obtener_factura(self, factura_id: int):
        return self.db.query(Factura)\
            .options(
                joinedload(Factura.paciente),
                joinedload(Factura.cliente),
                joinedload(Factura.lineas_factura)
                .joinedload(LineaFactura.linea_transaccional)
                .joinedload(LineaDocumentoTransaccional.linea_descargo)
            )\
            .filter(Factura.id == factura_id)\
            .first()

    def listar_facturas(self):
        return self.db.query(Factura)\
            .options(
                joinedload(Factura.paciente),
                joinedload(Factura.cliente),
                joinedload(Factura.lineas_factura)
                .joinedload(LineaFactura.linea_transaccional)
                .joinedload(LineaDocumentoTransaccional.linea_descargo)
            )\
            .all()