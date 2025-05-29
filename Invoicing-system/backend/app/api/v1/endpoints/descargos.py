from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.descargo_schema import DescargoCreate, DescargoResponse
from app.schemas.paciente_schema import PacienteConDescargosSimpleResponse
from app.services.descargo_service import DescargoService
from app.services.paciente_service import PacienteService
from app.core.database import get_db

router = APIRouter(prefix="/descargos", tags=["descargos"])

@router.post("/", response_model=DescargoResponse)
def crear_descargo(descargo: DescargoCreate, db: Session = Depends(get_db)):
    service = DescargoService(db)
    return service.crear_descargo(descargo)

@router.get("/paciente/{paciente_id}", response_model=list[DescargoResponse])
def listar_descargos_paciente(paciente_id: int, db: Session = Depends(get_db)):
    service = DescargoService(db)
    return service.obtener_descargos_paciente(paciente_id)

@router.get("/internados-con-descargos/", response_model=List[PacienteConDescargosSimpleResponse])
def listar_pacientes_internados_con_descargos(db: Session = Depends(get_db)):
    service = PacienteService(db)
    return service.obtener_pacientes_internados_con_descargos()

@router.get("/paciente/{paciente_id}", response_model=List[DescargoResponse])
def obtener_descargos_paciente(paciente_id: int, db: Session = Depends(get_db)):
    service = DescargoService(db)
    descargos = service.obtener_descargos_paciente(paciente_id)
    
    response_data = []
    for descargo in descargos:
        descargo_dict = {
            "id": descargo.id,
            "paciente_id": descargo.paciente_id,
            "fecha": descargo.fecha,
            "total": float(descargo.total) if descargo.total is not None else 0.0,
            "lineas": []
        }
        
        for linea_trans in descargo.lineas_transaccionales:
            if linea_trans.linea_descargo:
                linea_dict = {
                    "id": linea_trans.linea_descargo.id,
                    "descripcion": linea_trans.linea_descargo.descripcion,
                    "subtotal_sin_iva": float(linea_trans.linea_descargo.subtotal_sin_iva),
                    "cantidad": linea_trans.cantidad,
                    "servicio_id": linea_trans.servicio_id,
                    "producto_id": linea_trans.producto_id
                }
                descargo_dict["lineas"].append(linea_dict)
        
        response_data.append(descargo_dict)
    
    return response_data

@router.get("/buscar/", response_model=List[DescargoResponse])
def buscar_descargos(search: str = None, db: Session = Depends(get_db)):
    service = DescargoService(db)
    return service.buscar_descargos(search)

@router.get("/internados-con-descargos/")
def get_interned_patients_with_descargos(db: Session = Depends(get_db)):
    return DescargoService(db).get_interned_patients_with_descargos()

@router.get("/alta-con-descargos/")
def get_discharged_patients_with_descargos(db: Session = Depends(get_db)):
    return DescargoService(db).get_discharged_patients_with_descargos()