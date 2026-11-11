import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

class EmailFacturasService:
    def __init__(self):
        self.email_user = os.getenv("EMAIL_USER")
        self.email_pass = os.getenv("EMAIL_PASSWORD")
    
    def generar_pdf_factura(self, venta_id: int, cliente_nombre: str, detalles_compra: list, total: float) -> float:
        """"genera un arhivo pdf con la factura de la venta"""
        if not os.path.exists("facturas"):
            os.makedirs("facturas")
        
        filepath = f"facturas/factura_{venta_id}.pdf"
        doc = SimpleDocTemplate(filepath, pagesizes = letter)
        styles = getSampleStyleSheet()    
        story = [] 
        
        #creamos el encabezado de la factura
        story.append(Paragraph(f"<b> SUPERMARKET</b>", styles['title']))
        story.append(Paragraph(f"Factura de compra de {venta_id}", styles['Heading2']))   
        story.append(Paragraph(f"<b>cliente: </b> {cliente_nombre}", styles['Normal']))
        story.append(Spacer(1,15))
        
        #creo la tabla productos
        data = [["Producto", "Cantidad", "Precio Unitario", "Subtotal"]]
        for item in detalles_compra:
            data.append([
                item['nombre'],
                str(item['cantidad']),
                f"${item['precio']:.2f}",
                f"${item['subtotal']:.2f}"
            ])
        data.append(["", "", "TOTAL:", f"${total:.2f}"])

        tabla = Table(data, colWidths=[200, 80, 100, 100])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -2), 1, colors.grey),
            ('FONTNAME', (-2, -1), (-1, -1), 'Helvetica-Bold'),
        ]))

        story.append(tabla)
        story.append(Spacer(1, 20))
        story.append(Paragraph("¡Gracias por su compra en Supermarket Virtual!", styles['Italic']))

        doc.build(story)
        return filepath
    
    def enviar_factura_email(
        self,
        destino_email: str,
        cliente_nombre: str,
        venta_id: int,
        pdf_path: str,
    ):
        """Envía la factura en PDF adjunta por correo electrónico."""
        print(f"\nINICIANDO ENVÍO DE CORREO A {destino_email}...")

        if not self.email_user or not self.email_pass:
            print(
                f"ERROR CONFIGURACIÓN EMAIL: EMAIL_USER='{self.email_user}' o EMAIL_PASSWORD no encontrados en el .env"
            )
            return

        try:
            print(f"Conectando a servidor SMTP de Gmail...")
            msg = MIMEMultipart()
            msg["From"] = self.email_user
            msg["To"] = destino_email
            msg["Subject"] = f"Factura de Compra #{venta_id} - Supermarket Virtual"

            cuerpo = (
                f"Hola {cliente_nombre},\n\n"
                f"Adjunto encontrarás la factura correspondiente a tu compra realizada en Supermarket Virtual.\n\n"
                f"¡Gracias por tu preferencia!"
            )
            msg.attach(MIMEText(cuerpo, "plain"))

            with open(pdf_path, "rb") as f:
                adjunto = MIMEApplication(f.read(), _subtype="pdf")
                adjunto.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=os.path.basename(pdf_path),
                )
                msg.attach(adjunto)

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.email_user, self.email_pass)
            server.send_message(msg)
            server.quit()

            print(f"¡Factura enviada exitosamente a {destino_email}!")
        except Exception as e:
            print(f"ERROR SMTP al enviar el correo: {e}")       
        