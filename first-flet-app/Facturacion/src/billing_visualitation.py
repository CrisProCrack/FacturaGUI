import flet as ft
from flet import *
from billing import BillingManager
from datetime import datetime
from decimal import Decimal
from db_config import DatabaseConnection
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_billing_visualization_view(page: ft.Page):
    billing_manager = BillingManager()
    
    # Agregar esta constante al inicio de la función
    INVOICES_DIR = "facturas"
    # Crear la carpeta si no existe
    if not os.path.exists(INVOICES_DIR):
        os.makedirs(INVOICES_DIR)
    
    def select_invoice(invoice_id):
        page.show_snack_bar(SnackBar(content=Text(f"Factura {invoice_id} seleccionada")))

    def load_invoices():
        # Refrescar la conexión antes de obtener los datos
        billing_manager.conn = DatabaseConnection.get_connection()
        billing_manager.cursor = billing_manager.conn.cursor(dictionary=True)
        
        invoices = billing_manager.get_all_invoices()
        billing_table.rows.clear()
        
        for invoice in invoices:
            billing_table.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(str(invoice['id']))),
                        DataCell(Text(invoice['fecha'].strftime('%Y-%m-%d'))),
                        DataCell(Text(invoice['cliente_nombre'])),
                        DataCell(Text(f"${invoice['total']:,.2f}")),
                        DataCell(
                            IconButton(
                                icon=Icons.PRINT,
                                tooltip="Reimprimir factura",
                                data=invoice['id'],
                                on_click=lambda e: reprint_invoice(e.control.data)
                            )
                        ),
                    ],
                    on_select_changed=lambda e: select_invoice(e.control.cells[0].content.value)
                )
            )
        page.update()

    def reprint_invoice(invoice_data):
        try:
            # Ensure invoice data is valid
            if not invoice_data or 'total' not in invoice_data:
                raise ValueError("Invalid invoice data")

            # Convert total to Decimal if it isn't already
            total = Decimal(str(invoice_data['total'])) if not isinstance(invoice_data['total'], Decimal) else invoice_data['total']
            
            # Calculate totals
            subtotal = total / Decimal('1.19')
            iva = total - subtotal
            
            # Rest of your drawing code
            c.drawString(350, 200, f"Subtotal: ${subtotal:,.2f}")
            c.drawString(350, 180, f"IVA (19%): ${iva:,.2f}")
            c.drawString(350, 160, f"Total: ${total:,.2f}")
            
        except Exception as e:
            print(f"Error processing invoice: {str(e)}")

        invoice, details = billing_manager.get_invoice_details(invoice_data)
        if not invoice or not details:
            page.show_snack_bar(SnackBar(content=Text("Error al obtener los datos de la factura")))
            return

        # Generate PDF with new path
        pdf_path = os.path.join(INVOICES_DIR, f"factura_{invoice_data}_reprint.pdf")
        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "FACTURA - REIMPRESIÓN")
        c.drawString(450, 750, f"Folio: {invoice_data}")
        c.setFont("Helvetica", 12)
        c.drawString(50, 730, f"Fecha: {invoice['fecha'].strftime('%Y-%m-%d')}")
        
        # Customer info
        c.drawString(50, 700, f"Cliente: {invoice['nombre']}")
        c.drawString(50, 680, f"RFC: {invoice['rfc']}")
        c.drawString(50, 660, f"Dirección: {invoice['direccion']}")
        
        # Products table
        y = 600
        c.drawString(50, y, "Código")
        c.drawString(150, y, "Cant.")
        c.drawString(200, y, "Descripción")
        c.drawString(350, y, "P.Unit")
        c.drawString(450, y, "Total")
        
        y -= 20
        for detail in details:
            c.drawString(50, y, detail['codigo'])
            c.drawString(150, y, str(detail['cantidad']))
            c.drawString(200, y, detail['descripcion'])
            c.drawString(350, y, f"${detail['precio_unitario']:,.2f}")
            c.drawString(450, y, f"${detail['total']:,.2f}")
            y -= 20
        
        # Totals
        subtotal = invoice['total'] / Decimal('1.19')
        iva = invoice['total'] - subtotal
        
        c.drawString(350, 200, f"Subtotal: ${subtotal:,.2f}")
        c.drawString(350, 180, f"IVA (19%): ${iva:,.2f}")
        c.drawString(350, 160, f"Total: ${invoice['total']:,.2f}")
        
        c.save()
        
        # Open PDF
        os.startfile(pdf_path)
        page.show_snack_bar(SnackBar(content=Text("Factura reimpresa exitosamente")))

    # Tabla de facturas
    billing_table = DataTable(
        columns=[
            DataColumn(Text("Número")),
            DataColumn(Text("Fecha")),
            DataColumn(Text("Cliente")),
            DataColumn(Text("Total")),
            DataColumn(Text("Acciones")),
        ],
        rows=[],
    )

    def refresh_view(e):
        load_invoices()

    # Cargar facturas inicialmente
    load_invoices()

    return Container(
        content=Column(
            controls=[
                Text(
                    "Ver Facturas",
                    theme_style=TextThemeStyle.HEADLINE_LARGE,
                    weight=FontWeight.BOLD
                ),
                Divider(),            
                billing_table,
                Divider(),
                Row(
                    controls=[
                        ElevatedButton(
                            "Actualizar",
                            icon=Icons.REFRESH,
                            on_click=refresh_view
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
            ],
        ),
        padding=20,
        expand=True,
    )