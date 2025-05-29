from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status
from app.repositories.descargo_repository import DescargoRepository
from app.repositories.paciente_repository import PacienteRepository
from app.models.paciente import Paciente
from app.models.descargo import Descargo
from app.models.linea_transaccional import LineaDocumentoTransaccional
from app.schemas.descargo_schema import DescargoCreate, DescargoResponse

class DescargoService:
    def __init__(self, db):
        self.db = db  # Añadimos la sesión de la base de datos
        self.descargo_repo = DescargoRepository(db)
        self.paciente_repo = PacienteRepository(db)

    def crear_descargo(self, descargo_data: DescargoCreate):
        paciente = self.paciente_repo.obtener_por_id(descargo_data.paciente_id)
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
        if paciente.esta_facturado():
            raise HTTPException(
                status_code=400,
                detail="No se pueden agregar descargos a un paciente ya facturado"
            )

        # Validar que el paciente existe
        if not self.paciente_repo.obtener_por_id(descargo_data.paciente_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )
        
        # Validar al menos una línea
        if not descargo_data.lineas:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe incluir al menos una línea"
            )

        return self.descargo_repo.crear_descargo_con_lineas(
            descargo_data.paciente_id,
            descargo_data.lineas
        )
    
    def obtener_descargos_paciente(self, paciente_id: int):
        # Validar que el paciente existe
        if not self.paciente_repo.obtener_por_id(paciente_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )
    
        descargos = self.descargo_repo.obtener_descargos_por_paciente(paciente_id)
    
        # Asegurarse que todos los totales son float
        for descargo in descargos:
            if descargo.total is None:
                descargo.total = 0.0
            else:
                descargo.total = float(descargo.total)
    
        return descargos
    
    def get_interned_patients_with_descargos(self):
        pacientes = self.db.query(Paciente)\
            .filter(Paciente.estado == "internado")\
            .options(
                joinedload(Paciente.descargos)
                .joinedload(Descargo.lineas_transaccionales)
                .joinedload(LineaDocumentoTransaccional.linea_descargo)
            )\
            .all()

        pacientes_con_descargos = [p for p in pacientes if p.descargos]
        return pacientes_con_descargos

    def get_discharged_patients_with_descargos(self):
        pacientes = self.db.query(Paciente)\
            .filter(Paciente.estado == "alta")\
            .options(
                joinedload(Paciente.descargos)
                .joinedload(Descargo.lineas_transaccionales)
                .joinedload(LineaDocumentoTransaccional.linea_descargo)
            )\
            .all()

        pacientes_con_descargos = [p for p in pacientes if p.descargos]
        return pacientes_con_descargos