from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from emails.template import JinjaTemplate
import emails
import os

class PDFService:
    @staticmethod
    def generar_factura_pdf(factura_data: dict):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='RightAlign', alignment=2))
        
        story = []
        
        # Encabezado
        story.append(Paragraph("FACTURA", styles['Title']))
        story.append(Spacer(1, 12))
        
        # Información del cliente
        cliente = factura_data['cliente']
        cliente_info = [
            f"<b>Invoice to:</b>",
            f"{cliente['nombre']}",
            f"{cliente['direccion']}",
            f"{cliente['telefono']}",
            f"{cliente['correo']}"
        ]
        story.append(Paragraph("<br/>".join(cliente_info), styles['Normal']))
        story.append(Spacer(1, 24))
        
        # Tabla de productos
        data = [['CONSUMO', 'PRECIO', 'CANTIDAD', 'TOTAL']]
        for linea in factura_data['lineas']:
            data.append([
                linea['descripcion'],
                f"${linea['precio_unitario']:,.2f}",
                str(linea['cantidad']),
                f"${linea['total_con_iva']:,.2f}"
            ])
        
        t = Table(data, colWidths=[3*inch, inch, inch, inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(t)
        story.append(Spacer(1, 24))
        
        # Términos y condiciones
        story.append(Paragraph("<b>Términos & condiciones</b>", styles['Normal']))
        story.append(Paragraph(factura_data['factura']['terminos_condiciones'], styles['Normal']))
        story.append(Spacer(1, 24))
        
        # Totales
        data_totales = [
            ['SUBTOTAL', f"${factura_data['factura']['subtotal']:,.2f}"],
            ['IVA (16%)', f"${factura_data['factura']['impuesto']:,.2f}"],
            ['TOTAL', f"${factura_data['factura']['total_general']:,.2f}"]
        ]
        t_totales = Table(data_totales, colWidths=[4*inch, inch])
        t_totales.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black)
        ]))
        story.append(t_totales)
        story.append(Spacer(1, 36))
        
        # Pie de página
        hospital = factura_data['hospital']
        footer = [
            hospital['representante'],
            "",
            hospital['nombre'],
            hospital['direccion'],
            hospital['telefono'],
            hospital['email'],
            hospital['web']
        ]
        story.append(Paragraph("<br/>".join(footer), styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer

class EmailService:
    @staticmethod
    def enviar_factura(correo_destino: str, factura_data: dict, pdf_bytes: BytesIO):
        message = emails.html(
            subject=f"Factura #{factura_data['factura']['numero_factura']}",
            html=JinjaTemplate('''
                <p>Estimado {{ cliente.nombre }},</p>
                <p>Adjunto encontrará la factura #{{ factura.numero_factura }} por un total de ${{ "%.2f"|format(factura.total_general) }}.</p>
                <p>Fecha de emisión: {{ factura.fecha_emision.strftime('%d/%m/%Y') }}</p>
                <p>Gracias por su preferencia.</p>
                <p>Atentamente,<br/>{{ hospital.nombre }}</p>
            ''').render(cliente=factura_data['cliente'], factura=factura_data['factura'], hospital=factura_data['hospital']),
            mail_from=os.getenv('EMAIL_FROM', 'no-reply@hospital.com')
        )
        
        message.attach(
            filename=f"factura_{factura_data['factura']['numero_factura']}.pdf",
            content_disposition="attachment",
            data=pdf_bytes
        )
        
        return message.send(
            to=correo_destino,
            smtp={
                "host": os.getenv('SMTP_HOST'),
                "port": int(os.getenv('SMTP_PORT', 587)),
                "user": os.getenv('SMTP_USER'),
                "password": os.getenv('SMTP_PASSWORD'),
                "tls": True
            }
        )