from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.servicio_producto_schema import (
    ServicioCreate, 
    ServicioResponse,
    TipoServicioEnum
)
from app.services.servicio_service import ServicioService
from app.core.database import get_db

router = APIRouter(prefix="/servicios", tags=["servicios"])

@router.post("/", response_model=ServicioResponse)
def crear_servicio(servicio: ServicioCreate, db: Session = Depends(get_db)):
    return ServicioService(db).crear_servicio(servicio)

@router.get("/", response_model=list[ServicioResponse])
def listar_servicios(db: Session = Depends(get_db)):
    return ServicioService(db).listar_servicios()

@router.get("/{servicio_id}", response_model=ServicioResponse)
def obtener_servicio(servicio_id: int, db: Session = Depends(get_db)):
    return ServicioService(db).obtener_servicio(servicio_id)

@router.get("/tipo/{tipo}", response_model=list[ServicioResponse])
def listar_por_tipo(tipo: TipoServicioEnum, db: Session = Depends(get_db)):
    return ServicioService(db).listar_servicios(tipo=tipo)

@router.put("/{servicio_id}", response_model=ServicioResponse)
def actualizar_servicio(
    servicio_id: int, 
    servicio: ServicioCreate, 
    db: Session = Depends(get_db)
):
    return ServicioService(db).actualizar_servicio(servicio_id, servicio)

@router.delete("/{servicio_id}")
def eliminar_servicio(servicio_id: int, db: Session = Depends(get_db)):
    return ServicioService(db).eliminar_servicio(servicio_id)