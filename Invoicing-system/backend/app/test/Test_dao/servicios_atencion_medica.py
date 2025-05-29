def test_servicio_dao():
    db = next(get_test_db())
    
    # Crear atención médica
    atencion_data = {
        "id_servicio": "AT-001",
        "nombre": "Consulta Cardiológica",
        "costo": 150.00,
        "tipo": "atencion_medica",
        "medico": "Dr. Smith",
        "especialidad": "Cardiología",
        "duracion": 30
    }
    atencion = atencion_medica_dao.create(db, atencion_data)
    
    # Buscar por tipo
    atenciones = servicio_dao.get_by_type(db, "atencion_medica")
    assert len(atenciones) > 0
    
    # Buscar por especialidad
    cardiologos = atencion_medica_dao.get_by_especialidad(db, "Cardiología")
    assert len(cardiologos) > 0
    
    # Actualizar costo
    servicio_dao.update(db, atencion, {"costo": 175.00})
    assert atencion.costo == 175.00