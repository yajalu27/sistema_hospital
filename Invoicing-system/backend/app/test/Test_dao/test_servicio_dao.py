import pytest
from app.test.Test_dao.test_dao import get_test_db
from backend.app.models.servicios import AtencionMedica
from app.dao.base_dao import BaseDAO

atencion_dao = BaseDAO(AtencionMedica)

def test_servicio_dao():
    db = next(get_test_db())
    
    try:
        # Crear atención médica
        atencion_data = {
            "id_servicio": "SRV001",
            "nombre": "Consulta General",
            "costo": 150.00,
            "medico": "Dr. Smith",
            "especialidad": "Medicina General",
            "duracion": 30
        }
        atencion = atencion_dao.create(db, atencion_data)
        db.commit()

        # Verificar creación
        assert atencion.nombre == "Consulta General"
        assert float(atencion.costo) == 150.00
        assert atencion.medico == "Dr. Smith"
        assert atencion.especialidad == "Medicina General"
        assert atencion.duracion == 30

        # Buscar todos las atenciones médicas
        atenciones = db.query(AtencionMedica).all()
        assert len(atenciones) > 0

        # Actualizar costo
        atencion_dao.update(db, atencion, {"costo": 175.00})
        db.commit()
        assert float(atencion.costo) == 175.00

        # Eliminar servicio
        atencion_dao.delete(db, atencion.id_servicio)
        db.commit()
        assert atencion_dao.get(db, atencion.id_servicio) is None

    finally:
        db.rollback()
        db.close()