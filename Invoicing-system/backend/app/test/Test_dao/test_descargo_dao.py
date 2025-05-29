import pytest
from datetime import date
from app.test.Test_dao.test_dao import get_test_db
from app.models.paciente import Paciente
from app.models.consumo import ConsumoHospitalario, Descargos, LineaDescargo, Factura
from app.dao.base_dao import BaseDAO

paciente_dao = BaseDAO(Paciente)
consumo_dao = BaseDAO(ConsumoHospitalario)
descargo_dao = BaseDAO(Descargos)
linea_descargo_dao = BaseDAO(LineaDescargo)
factura_dao = BaseDAO(Factura)

def test_crear_descargo_completo():
    db = next(get_test_db())
    
    try:
        # Crear paciente
        paciente_data = {
            "id_paciente": "PAC001",
            "nombre": "Juan Pérez",
            "estado": "Alta",
            "fechaIngreso": date(2024, 3, 15),
            "fechaAlta": date(2024, 3, 20)
        }
        paciente = paciente_dao.create(db, paciente_data)
        
        # Crear consumo hospitalario
        consumo_data = {
            "id_consumo": "CON001",
            "tipo": "Servicio",
            "id_servicio": "SRV001",
            "fecha": date(2024, 3, 16),
            "descripcion": "Consulta médica",
            "costo": 150.00
        }
        consumo = consumo_dao.create(db, consumo_data)
        
        # Crear descargo
        descargo_data = {
            "id_descargo": "DES001",
            "id_paciente": paciente.id_paciente,
            "fecha_creacion": date(2024, 3, 20),
            "estado": "Pendiente"
        }
        descargo = descargo_dao.create(db, descargo_data)
        
        # Crear línea de descargo
        linea_descargo_data = {
            "id_linea_descargo": "LIN001",
            "id_descargo": descargo.id_descargo,
            "id_consumo_hospitalario": consumo.id_consumo,
            "cantidad": 1,
            "precioUnitario": consumo.costo
        }
        linea_descargo = linea_descargo_dao.create(db, linea_descargo_data)
        
        # Crear factura
        factura_data = {
            "id_factura": "FAC001",
            "id_descargo": descargo.id_descargo,
            "fecha": date(2024, 3, 20),
            "total": consumo.costo
        }
        factura = factura_dao.create(db, factura_data)
        
        db.commit()

        # Verificaciones
        print("\nDatos creados:")
        print(f"Paciente: {paciente.nombre} (ID: {paciente.id_paciente})")
        print(f"Consumo: {consumo.descripcion} - ${consumo.costo}")
        print(f"Descargo: {descargo.id_descargo} - Fecha: {descargo.fecha_creacion}")
        print(f"Línea de descargo: Cantidad: {linea_descargo.cantidad} - ${linea_descargo.precioUnitario}")
        print(f"Factura: {factura.id_factura} - Total: ${factura.total}")

        # Verificar relaciones
        assert descargo.id_paciente == paciente.id_paciente
        assert linea_descargo.id_descargo == descargo.id_descargo
        assert factura.id_descargo == descargo.id_descargo
        assert float(factura.total) == float(consumo.costo)

    finally:
        db.rollback()
        db.close()