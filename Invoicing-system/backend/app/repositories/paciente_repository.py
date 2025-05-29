from sqlalchemy.orm import Session, joinedload
from app.models.paciente import Paciente
from app.models.descargo import Descargo
from app.models.linea_transaccional import LineaDocumentoTransaccional
from app.models.linea_transaccional import LineaFactura, Factura
from sqlalchemy import func

class PacienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, paciente_id: int):
        return self.db.query(Paciente).filter(Paciente.id == paciente_id).first()

    def crear_paciente(self, paciente_data: dict):
        paciente = Paciente(**paciente_data)
        self.db.add(paciente)
        self.db.commit()
        self.db.refresh(paciente)
        return paciente

    def actualizar_paciente(self, paciente_id: int, paciente_data: dict):
        paciente = self.obtener_por_id(paciente_id)
        if paciente:
            for key, value in paciente_data.items():
                setattr(paciente, key, value)
            self.db.commit()
            self.db.refresh(paciente)
        return paciente

    def eliminar_paciente(self, paciente_id: int):
        paciente = self.obtener_por_id(paciente_id)
        if paciente:
            self.db.delete(paciente)
            self.db.commit()
        return paciente

    def set_alta(self, paciente_id: int):
        paciente = self.obtener_por_id(paciente_id)
        if paciente:
            paciente.estado = "alta"
            self.db.commit()
            self.db.refresh(paciente)
        return paciente

    def obtener_todos_pacientes(self):
        return self.db.query(Paciente).all()

    def buscar_pacientes(self, search_term: str = None):
        query = self.db.query(Paciente)
        if search_term:
            search_term = f"%{search_term}%"
            query = query.filter(
                (Paciente.nombre_completo.ilike(search_term))
            )
        return query.all()

    def obtener_pacientes_internados(self):
        return self.db.query(Paciente).filter(Paciente.estado == "internado").all()

    def obtener_descargos_paciente(self, paciente_id: int):
        return (
            self.db.query(Descargo)
            .filter(Descargo.paciente_id == paciente_id)
            .options(joinedload(Descargo.lineas_transaccionales))
            .all()
        )

    def obtener_pacientes_alta_con_descargos_no_facturados(self):
        # Subconsulta para obtener descargos que están asociados a facturas
        descargos_facturados = (
            self.db.query(LineaDocumentoTransaccional.descargo_id)
            .select_from(LineaDocumentoTransaccional)
            .join(LineaFactura, LineaDocumentoTransaccional.id == LineaFactura.linea_transaccional_id)
            .join(Factura, LineaFactura.factura_id == Factura.id)
            .distinct()
            .subquery()
        )

        # Consulta principal para obtener pacientes en estado "alta" con descargos no facturados
        pacientes = (
            self.db.query(Paciente)
            .select_from(Paciente)
            .join(Descargo, Paciente.id == Descargo.paciente_id)
            .filter(Paciente.estado == "alta")
            .filter(~Descargo.id.in_(descargos_facturados))
            .options(
                joinedload(Paciente.descargos).joinedload(Descargo.lineas_transaccionales)
            )
            .distinct()
            .all()
        )
        return pacientes