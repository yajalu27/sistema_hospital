from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.servicio_producto_schema import (
    ProductoCreate, 
    ProductoResponse,
    TipoProductoEnum
)
from app.services.producto_service import ProductoService
from app.core.database import get_db

router = APIRouter(prefix="/productos", tags=["productos"])

@router.post("/", response_model=ProductoResponse)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    return ProductoService(db).crear_producto(producto)

@router.get("/", response_model=list[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return ProductoService(db).listar_productos()

@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    return ProductoService(db).obtener_producto(producto_id)

@router.get("/tipo/{tipo}", response_model=list[ProductoResponse])
def listar_por_tipo(tipo: TipoProductoEnum, db: Session = Depends(get_db)):
    return ProductoService(db).listar_productos(tipo=tipo)

@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: int, 
    producto: ProductoCreate, 
    db: Session = Depends(get_db)
):
    return ProductoService(db).actualizar_producto(producto_id, producto)

@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    return ProductoService(db).eliminar_producto(producto_id)