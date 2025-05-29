from sqlalchemy.orm import Session, joinedload
from app.models import Factura, LineaFactura, LineaDocumentoTransaccional

class FacturaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_factura(self, factura_data, lineas_data):
        factura = Factura(**factura_data)
        self.db.add(factura)
        self.db.commit()
        self.db.refresh(factura)

        for linea_data in lineas_data:
            linea_factura = LineaFactura(factura_id=factura.id, **linea_data)
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