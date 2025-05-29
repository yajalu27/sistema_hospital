from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import (
    pacientes,
    descargos,
    servicios,
    productos,
    clientes,
    facturas
)

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, reemplaza "*" con tu dominio frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pacientes.router)
app.include_router(descargos.router)
app.include_router(servicios.router)
app.include_router(productos.router)
app.include_router(clientes.router)
app.include_router(facturas.router)

@app.get("/")
def read_root():
    return {"message":"Sistema de facturacion Hospitalaria"}