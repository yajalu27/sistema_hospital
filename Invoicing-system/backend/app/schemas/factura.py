from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class LineaFacturaResponse(BaseModel):
    descripcion: str
    cantidad: int
    subtotal_sin_iva: float
    iva: float
    total_con_iva: float
    precio_unitario: float

    class Config:
        schema_extra = {
            "example": {
                "descripcion": "Servicio: Consulta especializada",
                "cantidad": 1,
                "subtotal_sin_iva": 500.0,
                "iva": 80.0,
                "total_con_iva": 580.0,
                "precio_unitario": 500.0
            }
        }

class FacturaResponse(BaseModel):
    factura: dict
    paciente: dict
    cliente: dict
    lineas: List[LineaFacturaResponse]

    class Config:
        schema_extra = {
            "example": {
                "factura": {
                    "id": 1,
                    "numero_factura": "FACT-20230501-0001",
                    "fecha_emision": "2023-05-01T10:30:00",
                    "subtotal": 1000.0,
                    "impuesto": 160.0,
                    "total_general": 1160.0,
                    "estado_pago": "pendiente"
                },
                "paciente": {
                    "id": 1,
                    "nombre_completo": "Juan Pérez",
                    "fecha_ingreso": "2023-04-15T08:00:00",
                    "fecha_alta": "2023-04-30T12:00:00",
                    "afeccion": "Fractura de brazo"
                },
                "cliente": {
                    "id": 1,
                    "nombre": "Seguros XYZ",
                    "direccion": "Av. Principal 123",
                    "telefono": "555-1234",
                    "correo": "contacto@segurosxyz.com"
                },
                "lineas": [
                    {
                        "descripcion": "Servicio: Consulta especializada",
                        "cantidad": 1,
                        "subtotal_sin_iva": 500.0,
                        "iva": 80.0,
                        "total_con_iva": 580.0,
                        "precio_unitario": 500.0  # Agregado
                    },
                    {
                        "descripcion": "Producto: Yeso ortopédico",
                        "cantidad": 1,
                        "subtotal_sin_iva": 500.0,
                        "iva": 80.0,
                        "total_con_iva": 580.0,
                        "precio_unitario": 500.0  # Agregado
                    }
                ]
            }
        }