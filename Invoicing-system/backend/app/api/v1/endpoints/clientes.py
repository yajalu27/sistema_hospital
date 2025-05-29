from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.services.cliente_service import ClienteService
from app.core.database import get_db

router = APIRouter(prefix="/clientes", tags=["clientes"])

@router.post("/", response_model=ClienteResponse)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return ClienteService(db).create_cliente(cliente)

@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = ClienteService(db).get_cliente(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return cliente

@router.get("/", response_model=list[ClienteResponse])
def list_clientes(db: Session = Depends(get_db)):
    return ClienteService(db).list_clientes()

@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(cliente_id: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    updated_cliente = ClienteService(db).update_cliente(cliente_id, cliente)
    if not updated_cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return updated_cliente

@router.delete("/{cliente_id}", response_model=ClienteResponse)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    deleted_cliente = ClienteService(db).delete_cliente(cliente_id)
    if not deleted_cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return deleted_cliente