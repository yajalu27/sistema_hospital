from sqlalchemy.orm import Session
from app.repositories.paciente_repository import PacienteRepository
from app.schemas.paciente_schema import PacienteCreate, PacienteResponse, PacienteConDescargosSimpleResponse

class PacienteService:
    def __init__(self, db: Session):
        self.repo = PacienteRepository(db)

    def set_alta(self, paciente_id: int):
        return self.repo.set_alta(paciente_id)

    def crear_paciente(self, paciente: PacienteCreate):
        return self.repo.crear_paciente(paciente.model_dump())

    def obtener_paciente(self, paciente_id: int):
        return self.repo.obtener_por_id(paciente_id)

    def actualizar_paciente(self, paciente_id: int, paciente: PacienteCreate):
        return self.repo.actualizar_paciente(paciente_id, paciente.model_dump())

    def eliminar_paciente(self, paciente_id: int):
        return self.repo.eliminar_paciente(paciente_id)

    def obtener_todos_pacientes(self):
        return self.repo.obtener_todos_pacientes()

    def buscar_pacientes(self, search_term: str = None):
        return self.repo.buscar_pacientes(search_term)

    def obtener_pacientes_internados_con_descargos(self):
        pacientes = self.repo.obtener_pacientes_internados()
        print("Pacientes internados encontrados:", pacientes)
        
        result = []
        for paciente in pacientes:
            descargos = self.repo.obtener_descargos_paciente(paciente.id)
            print(f"Descargos para paciente {paciente.id} ({paciente.nombre_completo}):", descargos)
            if descargos:
                paciente_dict = {
                    "id": paciente.id,
                    "nombre_completo": paciente.nombre_completo,
                    "fecha_ingreso": paciente.fecha_ingreso,
                    "estado": paciente.estado,
                    "descargos": [
                        {
                            "id": descargo.id,
                            "paciente_id": descargo.paciente_id,
                            "fecha": descargo.fecha,
                            "total": float(descargo.total) if descargo.total is not None else 0.0,
                            "lineas": [
                                {
                                    "id": linea_trans.linea_descargo.id,
                                    "descripcion": linea_trans.linea_descargo.descripcion,
                                    "subtotal_sin_iva": float(linea_trans.linea_descargo.subtotal_sin_iva),
                                    "cantidad": linea_trans.cantidad,
                                    "servicio_id": linea_trans.servicio_id,
                                    "producto_id": linea_trans.producto_id
                                }
                                for linea_trans in descargo.lineas_transaccionales
                                if linea_trans.linea_descargo
                            ]
                        }
                        for descargo in descargos
                    ]
                }
                result.append(PacienteConDescargosSimpleResponse(**paciente_dict))
        
        print("Resultado final:", result)
        return result

    def obtener_pacientes_alta_con_descargos_no_facturados(self):
        pacientes = self.repo.obtener_pacientes_alta_con_descargos_no_facturados()
        print("Pacientes en alta con descargos no facturados encontrados:", pacientes)
        
        result = []
        for paciente in pacientes:
            descargos = [descargo for descargo in paciente.descargos]
            if descargos:
                paciente_dict = {
                    "id": paciente.id,
                    "nombre_completo": paciente.nombre_completo,
                    "fecha_ingreso": paciente.fecha_ingreso,
                    "fecha_alta": paciente.fecha_alta,
                    "estado": paciente.estado,
                    "descargos": [
                        {
                            "id": descargo.id,
                            "paciente_id": descargo.paciente_id,
                            "fecha": descargo.fecha,
                            "total": float(descargo.total) if descargo.total is not None else 0.0,
                            "lineas": [
                                {
                                    "id": linea_trans.linea_descargo.id,
                                    "descripcion": linea_trans.linea_descargo.descripcion,
                                    "subtotal_sin_iva": float(linea_trans.linea_descargo.subtotal_sin_iva),
                                    "cantidad": linea_trans.cantidad,
                                    "servicio_id": linea_trans.servicio_id,
                                    "producto_id": linea_trans.producto_id
                                }
                                for linea_trans in descargo.lineas_transaccionales
                                if linea_trans.linea_descargo
                            ]
                        }
                        for descargo in descargos
                    ]
                }
                result.append(PacienteConDescargosSimpleResponse(**paciente_dict))
        
        print("Resultado final:", result)
        return result