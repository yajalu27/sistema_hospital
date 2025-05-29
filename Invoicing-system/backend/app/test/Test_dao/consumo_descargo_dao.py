def test_consumo_descargos_dao():
    db = next(get_test_db())
    
    # Crear paciente y producto
    paciente = paciente_dao.create(db, {
        "nombre": "María González",
        "estado": "Internado"
    })
    
    producto = producto_dao.create(db, {
        "id_producto": "MED-001",
        "nombre": "Ibuprofeno",
        "precio": 5.99,
        "tipo": "medicamento"
    })
    
    # Crear consumo hospitalario
    consumo_data = {
        "id_consumo": "CONS-001",
        "tipo": "Producto",
        "id_producto": producto.id_producto,
        "fecha": "2023-01-15",
        "descripcion": "Medicamento para dolor",
        "costo": 5.99
    }
    consumo = consumo_hospitalario_dao.create(db, consumo_data)
    
    # Crear descargo
    descargo_data = {
        "id_descargo": "DESC-001",
        "id_paciente": paciente.id_paciente,
        "fecha_creacion": "2023-01-15",
        "estado": "Pendiente"
    }
    descargo = descargos_dao.create(db, descargo_data)
    
    # Crear línea de descargo
    linea_data = {
        "id_linea_descargo": "LINEA-001",
        "id_descargo": descargo.id_descargo,
        "id_consumo_hospitalario": consumo.id_consumo,
        "cantidad": 2,
        "precioUnitario": 5.99
    }
    linea_descargo_dao.create(db, linea_data)
    
    # Verificar total
    total = descargos_dao.get_total_amount(db, descargo.id_descargo)
    assert total == 11.98  # 2 * 5.99
    
    # Crear factura
    factura_data = {
        "id_factura": "FACT-001",
        "id_descargo": descargo.id_descargo,
        "fecha": "2023-01-16",
        "total": total
    }
    factura = factura_dao.create(db, factura_data)
    
    # Verificar relación
    assert factura.descargo.id_paciente == paciente.id_paciente