import pytest
from datetime import date
from app.test.Test_dao.test_dao import get_test_db
from app.models.producto import Medicamento
from app.dao.base_dao import BaseDAO

medicamento_dao = BaseDAO(Medicamento)

def test_producto_dao():
    db = next(get_test_db())
    
    try:
        # Crear producto
        producto_data = {
            "nombre": "Producto Test",
            "precio": 10.99,
            "tipo": "producto"
        }
        producto = producto_dao.create(db, producto_data)
        db.commit()

        # Verificar creación
        assert producto.nombre == "Producto Test"
        assert float(producto.precio) == 10.99
        
        # Buscar por tipo
        productos = producto_dao.get_by_type(db, "producto")
        assert len(productos) > 0

        # Eliminar producto
        producto_dao.delete(db, producto.id_producto)
        db.commit()
        assert producto_dao.get(db, producto.id_producto) is None

    finally:
        db.rollback()
        db.close()


def test_producto_dao():
    db = next(get_test_db())
    
    try:
        # Crear medicamento
        medicamento_data = {
            "id_producto": "MED001",
            "nombre": "Paracetamol",
            "precio": 10.99,
            "laboratorio": "Bayer",
            "dosis": "500mg"
        }
        medicamento = medicamento_dao.create(db, medicamento_data)
        db.commit()

        # Verificar creación
        assert medicamento.nombre == "Paracetamol"
        assert float(medicamento.precio) == 10.99
        assert medicamento.laboratorio == "Bayer"
        assert medicamento.dosis == "500mg"

        # Buscar todos los medicamentos
        medicamentos = db.query(Medicamento).all()
        assert len(medicamentos) > 0

        # Actualizar precio
        medicamento_dao.update(db, medicamento, {"precio": 12.99})
        db.commit()
        assert float(medicamento.precio) == 12.99

        # Eliminar medicamento
        medicamento_dao.delete(db, medicamento.id_producto)
        db.commit()
        assert medicamento_dao.get(db, medicamento.id_producto) is None

    finally:
        db.rollback()
        db.close()