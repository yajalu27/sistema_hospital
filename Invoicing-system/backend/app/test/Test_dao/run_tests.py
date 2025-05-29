import pytest
from test_paciente_dao import test_paciente_dao
from test_producto_dao import test_producto_dao
from test_servicio_dao import test_servicio_dao
from test_consumo_descargo_dao import test_consumo_descargos_dao

if __name__ == "__main__":
    pytest.main([
        "test_paciente_dao.py",
        "test_producto_dao.py",
        "test_servicio_dao.py",
        "test_consumo_descargo_dao.py",
        "-v"
    ])


