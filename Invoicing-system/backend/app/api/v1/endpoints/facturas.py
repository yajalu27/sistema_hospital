import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.services.factura_service import FacturaService
from app.core.database import get_db
from app.schemas.factura import FacturaResponse
from app.services.pdf_service import PDFService, EmailService

router = APIRouter(prefix="/facturas", tags=["facturas"])

@router.post("/generar/{paciente_id}/{cliente_id}", response_model=dict)
def generar_factura(paciente_id: int, cliente_id: int, db: Session = Depends(get_db)):
    service = FacturaService(db)
    try:
        factura_data = service.generar_factura(paciente_id, cliente_id)
        
        # Generar PDF
        pdf_service = PDFService()
        pdf_bytes = pdf_service.generar_factura_pdf(factura_data)
        
        # Enviar por correo
        if os.getenv('ENABLE_EMAIL', 'false').lower() == 'true':
            email_service = EmailService()
            email_service.enviar_factura(
                factura_data['cliente']['correo'],
                factura_data,
                pdf_bytes
            )
        
        return factura_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{factura_id}", response_model=dict)
def obtener_factura(factura_id: int, db: Session = Depends(get_db)):
    service = FacturaService(db)
    try:
        return service.obtener_factura(factura_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{factura_id}/pdf")
def descargar_factura_pdf(factura_id: int, db: Session = Depends(get_db)):
    service = FacturaService(db)
    try:
        factura_data = service.obtener_factura(factura_id)
        pdf_service = PDFService()
        pdf_bytes = pdf_service.generar_factura_pdf(factura_data)
        
        return StreamingResponse(
            pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=factura_{factura_data['factura']['numero_factura']}.pdf"
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[dict])
def listar_facturas(db: Session = Depends(get_db)):
    service = FacturaService(db)
    try:
        return service.listar_facturas()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))