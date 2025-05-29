from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class LineaDocumentoTransaccional(Base):
    __tablename__ = "lineas_transaccionales"
    
    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer, default=1)
    descargo_id = Column(Integer, ForeignKey("descargos.id"))
    servicio_id = Column(Integer, ForeignKey("servicios.id"), nullable=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=True)
    
    # Relaciones
    descargo = relationship("Descargo", back_populates="lineas_transaccionales")
    servicio = relationship("Servicio")
    producto = relationship("Producto")
    
    # Relación uno-a-uno con LineaDescargo
    linea_descargo = relationship(
        "LineaDescargo", 
        back_populates="linea_transaccional", 
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    # Relación uno-a-uno con LineaFactura
    linea_factura = relationship(
        "LineaFactura", 
        back_populates="linea_transaccional", 
        uselist=False,
        cascade="all, delete-orphan"
    )

class LineaDescargo(Base):
    __tablename__ = "lineas_descargo"
    
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(200))
    subtotal_sin_iva = Column(Float)
    linea_transaccional_id = Column(
        Integer, 
        ForeignKey("lineas_transaccionales.id"), 
        unique=True  # Para relación uno-a-uno
    )
    
    linea_transaccional = relationship(
        "LineaDocumentoTransaccional", 
        back_populates="linea_descargo"
    )

class LineaFactura(Base):
    __tablename__ = 'lineas_factura'
    
    id = Column(Integer, primary_key=True, index=True)
    iva = Column(Float, default=0.16)
    total_con_iva = Column(Float)
    
    # Clave foránea para relación con LineaDocumentoTransaccional
    linea_transaccional_id = Column(
        Integer, 
        ForeignKey('lineas_transaccionales.id'), 
        unique=True  # Para relación uno-a-uno
    )
    
    # Clave foránea para relación con Factura
    factura_id = Column(Integer, ForeignKey('facturas.id'))
    
    # Relaciones
    factura = relationship("Factura", back_populates="lineas_factura")
    linea_transaccional = relationship(
        "LineaDocumentoTransaccional", 
        back_populates="linea_factura"
    )

class Factura(Base):
    __tablename__ = 'facturas'
    
    id = Column(Integer, primary_key=True, index=True)
    numero_factura = Column(String(50), unique=True)
    fecha_emision = Column(DateTime, default=datetime.utcnow)
    subtotal = Column(Float)
    impuesto = Column(Float)
    total_general = Column(Float)
    estado_pago = Column(String(20), default="pendiente")
    terminos_condiciones = Column(String(500))
    
    # Claves foráneas
    paciente_id = Column(Integer, ForeignKey('pacientes.id'))
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    
    # Relaciones
    paciente = relationship("Paciente", back_populates="facturas")
    cliente = relationship("Cliente", back_populates="facturas")
    lineas_factura = relationship(
        "LineaFactura", 
        back_populates="factura",
        cascade="all, delete-orphan"
    )