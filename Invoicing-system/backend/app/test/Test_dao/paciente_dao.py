def test_paciente_dao():
    db = next(get_test_db())
    
    # Crear paciente
    paciente_data = {
        "nombre": "Juan Pérez",
        "estado": "Internado",
        "fechaIngreso": "2023-01-15"
    }
    paciente = paciente_dao.create(db, paciente_data)
    
    # Buscar por nombre
    pacientes = paciente_dao.get_by_name(db, "Juan")
    assert len(pacientes) > 0
    
    # Buscar por estado
    internados = paciente_dao.get_active_patients(db)
    assert any(p.nombre == "Juan Pérez" for p in internados)
    
    # Actualizar
    paciente_dao.update(db, paciente, {"estado": "Alta", "fechaAlta": "2023-01-20"})
    assert paciente.estado == "Alta"
    
    # Eliminar
    paciente_dao.delete(db, paciente.id_paciente)
    assert paciente_dao.get(db, paciente.id_paciente) is None