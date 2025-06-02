from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.paciente_service import PacienteService
from app.schemas.paciente_schema import PacienteCreate, PacienteResponse, PacienteConDescargosSimpleResponse
from app.core.database import get_db

router = APIRouter(prefix="/pacientes", tags=["pacientes"])

@router.get("/listar_pacientes/", response_model=list[PacienteResponse])
def get_patients(db: Session = Depends(get_db)):
    return PacienteService(db).obtener_todos_pacientes()

@router.get("/buscar_paciente/", response_model=list[PacienteResponse])
def search_patients(search: str = None, db: Session = Depends(get_db)):
    return PacienteService(db).buscar_pacientes(search)

@router.post("/crear_paciente/", response_model=PacienteResponse)
def create_patient(paciente: PacienteCreate, db: Session = Depends(get_db)):
    return PacienteService(db).crear_paciente(paciente)

@router.get("/{paciente_id}", response_model=PacienteResponse)
def get_patient(paciente_id: int, db: Session = Depends(get_db)):
    paciente = PacienteService(db).obtener_paciente(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

@router.put("/{paciente_id}", response_model=PacienteResponse)
def update_patient(paciente_id: int, paciente: PacienteCreate, db: Session = Depends(get_db)):
    updated_paciente = PacienteService(db).actualizar_paciente(paciente_id, paciente)
    if not updated_paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return updated_paciente

@router.delete("/{paciente_id}")
def delete_patient(paciente_id: int, db: Session = Depends(get_db)):
    paciente = PacienteService(db).eliminar_paciente(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"detail": "Paciente eliminado"}

@router.patch("/daralta_paciente/{paciente_id}/alta", response_model=PacienteResponse)
def discharge_patient(paciente_id: int, db: Session = Depends(get_db)):
    paciente = PacienteService(db).set_alta(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

@router.get("/internados-con-descargos/", response_model=list[PacienteConDescargosSimpleResponse])
def get_interned_patients_with_discharges(db: Session = Depends(get_db)):
    return PacienteService(db).obtener_pacientes_internados_con_descargos()

@router.get("/alta-con-descargos-no-facturados/", response_model=list[PacienteConDescargosSimpleResponse])
def get_discharged_patients_with_unbilled_discharges(db: Session = Depends(get_db)):
    return PacienteService(db).obtener_pacientes_alta_con_descargos_no_facturados()

@router.post("/{paciente_id}/agregar_descargo/", response_model=PacienteResponse)
def add_discharge(paciente_id: int, descargo_data: dict, db: Session = Depends(get_db)):
    paciente = PacienteService(db).set_alta(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    descargo = PacienteService(db).repo.agregar_descargo(paciente_id, descargo_data)
    if descargo is None:
        raise HTTPException(status_code=400, detail="No se pudo agregar el descargo")
    return paciente

@router.post("/{paciente_id}/facturar/", response_model=PacienteResponse)
def bill_patient(paciente_id: int, factura_data: dict, db: Session = Depends(get_db)):
    paciente = PacienteService(db).obtener_paciente(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    factura = PacienteService(db).repo.facturar(paciente_id, factura_data)
    if factura is None:
        raise HTTPException(status_code=400, detail="No se pudo facturar")
    return paciente