from app.models.linea_transaccional import LineaDocumentoTransaccional, LineaDescargo, LineaFactura

# Prototipo base para LineaDocumentoTransaccional
linea_transaccional_prototype_servicio = LineaDocumentoTransaccional(
    cantidad=1,
    servicio_id=None,
    producto_id=None
)

linea_transaccional_prototype_producto = LineaDocumentoTransaccional(
    cantidad=1,
    servicio_id=None,
    producto_id=None
)

# Prototipo base para LineaDescargo
linea_descargo_prototype = LineaDescargo(
    descripcion="Descripción genérica",
    subtotal_sin_iva=0.0
)

# Prototipo base para LineaFactura
linea_factura_prototype = LineaFactura(
    iva=0.16,
    total_con_iva=0.0
)