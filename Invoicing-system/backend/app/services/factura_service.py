from fastapi import HTTPException
from datetime import datetime
from app.repositories.factura_repository import FacturaRepository
from app.repositories.paciente_repository import PacienteRepository
from app.repositories.cliente_repository import ClienteRepository 
from app.repositories.descargo_repository import DescargoRepository

class FacturaService:
    def __init__(self, db):
        self.db = db
        self.repo = FacturaRepository(db)
        self.paciente_repo = PacienteRepository(db)
        self.cliente_repo = ClienteRepository(db)
        self.descargo_repo = DescargoRepository(db)

    def generar_factura(self, paciente_id: int, cliente_id: int):
        try:
            # 1. Validar paciente
            paciente = self.paciente_repo.obtener_por_id(paciente_id)
            if not paciente:
                raise HTTPException(status_code=404, detail="Paciente no encontrado")
            if paciente.estado != "alta":
                raise HTTPException(status_code=400, detail="El paciente no se encuentra en estado de alta")
            
            # 2. Validar cliente
            cliente = self.cliente_repo.get(cliente_id)
            if not cliente:
                raise HTTPException(status_code=404, detail="Cliente no encontrado")
            
            # 3. Obtener descargos
            descargos = self.descargo_repo.obtener_descargos_por_paciente(paciente_id)
            if not descargos:
                raise HTTPException(status_code=400, detail="El paciente no tiene descargos para facturar")
            
            # 4. Calcular totales y preparar líneas de factura
            subtotal = 0.0
            impuesto = 0.0
            lineas_factura = []
            
            for descargo in descargos:
                for linea_trans in descargo.lineas_transaccionales:
                    if not (linea_trans and linea_trans.linea_descargo and linea_trans.cantidad and linea_trans.cantidad > 0):
                        continue
                    
                    subtotal_linea = linea_trans.linea_descargo.subtotal_sin_iva or 0
                    iva = subtotal_linea * 0.16  # Asumiendo 16% de IVA
                    total_con_iva = subtotal_linea + iva
                    
                    subtotal += subtotal_linea
                    impuesto += iva
                    
                    linea_factura = {
                        "linea_transaccional_id": linea_trans.id,
                        "iva": iva,
                        "total_con_iva": total_con_iva
                    }
                    lineas_factura.append(linea_factura)
            
            if not lineas_factura:
                raise HTTPException(status_code=400, detail="No hay líneas válidas para facturar")
            
            total_general = subtotal + impuesto
            
            # 5. Generar número de factura
            numero_factura = f"FACT-{datetime.now().strftime('%Y%m%d')}-{paciente_id:04d}"
            
            # 6. Preparar datos de factura
            factura_data = {
                "numero_factura": numero_factura,
                "fecha_emision": datetime.now(),
                "subtotal": subtotal,
                "impuesto": impuesto,
                "total_general": total_general,
                "paciente_id": paciente_id,
                "cliente_id": cliente_id,
                "estado_pago": "pendiente",
                "terminos_condiciones": "Pago dentro de 30 días"
            }
            
            # 7. Crear factura en el repositorio
            factura = self.repo.create_factura(factura_data, lineas_factura)
            
            # 8. Preparar respuesta
            return self._prepare_factura_response(factura, paciente, cliente)
            
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al generar factura: {str(e)}")

    def obtener_factura(self, factura_id: int):
        try:
            factura = self.repo.obtener_factura(factura_id)
            if not factura:
                raise HTTPException(status_code=404, detail="Factura no encontrada")
            return self._prepare_factura_response(factura, factura.paciente, factura.cliente)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener factura: {str(e)}")

    def listar_facturas(self):
        try:
            facturas = self.repo.listar_facturas()
            return [
                self._prepare_factura_response(factura, factura.paciente, factura.cliente)
                for factura in facturas
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al listar facturas: {str(e)}")

    def _prepare_factura_response(self, factura, paciente, cliente):
        """Método auxiliar para preparar la respuesta de la factura"""
        lineas = []
        for linea in factura.lineas_factura:
            linea_data = {
                "descripcion": "",
                "cantidad": 0,
                "precio_unitario": 0.0,
                "subtotal_sin_iva": 0.0,
                "iva": linea.iva or 0,
                "total_con_iva": linea.total_con_iva or 0
            }
            
            if linea.linea_transaccional and linea.linea_transaccional.linea_descargo:
                descripcion = linea.linea_transaccional.linea_descargo.descripcion or ""
                cantidad = linea.linea_transaccional.cantidad or 0
                subtotal_sin_iva = linea.linea_transaccional.linea_descargo.subtotal_sin_iva or 0
                precio_unitario = subtotal_sin_iva / cantidad if cantidad > 0 else 0.0
                
                linea_data.update({
                    "descripcion": descripcion,
                    "cantidad": cantidad,
                    "precio_unitario": precio_unitario,
                    "subtotal_sin_iva": subtotal_sin_iva
                })
            
            lineas.append(linea_data)
        
        return {
            "factura": {
                "id": factura.id,
                "numero_factura": factura.numero_factura,
                "fecha_emision": factura.fecha_emision,
                "subtotal": factura.subtotal,
                "impuesto": factura.impuesto,
                "total_general": factura.total_general,
                "estado_pago": factura.estado_pago,
                "terminos_condiciones": factura.terminos_condiciones or "",
                "paciente_id": factura.paciente_id,
                "cliente_id": factura.cliente_id
            },
            "paciente": {
                "id": paciente.id,
                "nombre_completo": paciente.nombre_completo or "",
                "fecha_ingreso": paciente.fecha_ingreso,
                "fecha_alta": paciente.fecha_alta,
                "afeccion": paciente.afeccion or ""
            },
            "cliente": {
                "id": cliente.id,
                "nombre": cliente.nombre or "",
                "direccion": cliente.direccion or "",
                "telefono": cliente.telefono or "",
                "correo": cliente.correo or ""
            },
            "lineas": lineas,
            "hospital": {
                "nombre": "Hospital Ejemplo",
                "direccion": "Health District, 123 Streets, Sopporo, Hokkaido",
                "telefono": "+123 456 789",
                "email": "hello@email.com",
                "web": "www.yourweb.com",
                "representante": "Dr. Ramiela Silva, MD, PHD - General Manager"
            }
        }