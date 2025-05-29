import pytest
from datetime import datetime, date
from app.test.Test_dao.test_dao import get_test_db
from app.repositories import paciente_dao

def test_paciente_dao():
    db = next(get_test_db())
    
    try:
        # Crear paciente
        paciente_data = {
            "nombre": "Juan Pérez",
            "estado": "Internado",
            "fechaIngreso": date(2023, 1, 15)
        }
        paciente = paciente_dao.create(db, paciente_data)
        db.commit()

        # Verificar creación
        assert paciente.nombre == "Juan Pérez"
        assert paciente.estado == "Internado"
        assert paciente.fechaIngreso == date(2023, 1, 15)
        
        # Buscar por nombre
        pacientes = paciente_dao.get_by_name(db, "Juan")
        assert len(pacientes) > 0
        assert pacientes[0].nombre == "Juan Pérez"
        
        # Buscar por estado
        internados = paciente_dao.get_active_patients(db)
        assert any(p.nombre == "Juan Pérez" for p in internados)
        
        # Actualizar estado
        paciente_dao.update(db, paciente, {
            "estado": "Alta",
            "fechaAlta": date(2023, 1, 20)  # Use date object here too
        })
        db.commit()  # Add commit after update
        
        assert paciente.estado == "Alta"
        assert paciente.fechaAlta == date(2023, 1, 20)
        
        # Verificar actualización
        paciente_actualizado = paciente_dao.get(db, paciente.id_paciente)
        assert paciente_actualizado.estado == "Alta"
        
        # Eliminar
        paciente_dao.delete(db, paciente.id_paciente)
        db.commit()  # Add commit after delete
        
        assert paciente_dao.get(db, paciente.id_paciente) is None

    finally:
        db.rollback()  # Rollback any uncommitted changes
        db.close()