def test_producto_dao():
    db = next(get_test_db())
    
    # Crear producto genérico
    producto_data = {
        "id_producto": "PROD-001",
        "nombre": "Producto Genérico",
        "precio": 10.99,
        "tipo": "producto"
    }
    producto = producto_dao.create(db, producto_data)
    
    # Crear vacuna
    vacuna_data = {
        "id_producto": "VAC-001",
        "nombre": "Vacuna COVID",
        "precio": 25.50,
        "tipo": "vacuna",
        "tipoVacuna": "ARNm",
        "lote": "LOTE-2023",
        "fechaCaducidad": "2024-12-31"
    }
    vacuna = vacuna_dao.create(db, vacuna_data)
    
    # Buscar por tipo
    vacunas = producto_dao.get_by_type(db, "vacuna")
    assert len(vacunas) > 0
    
    # Buscar por rango de precio
    productos = producto_dao.get_by_price_range(db, 20.0, 30.0)
    assert any(p.nombre == "Vacuna COVID" for p in productos)
    
    # Métodos específicos de VacunaDAO
    vacunas_por_lote = vacuna_dao.get_by_lote(db, "LOTE-2023")
    assert len(vacunas_por_lote) > 0