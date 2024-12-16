import flet as ft
from flet import *
from datetime import datetime
from db_config import DatabaseConnection
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

class BillingManager:
    def __init__(self):
        self.conn = DatabaseConnection.get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    def get_all_customers(self):
        self.cursor.execute("SELECT * FROM clientes")
        return self.cursor.fetchall()

    def get_customer_by_id(self, id):
        self.cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
        return self.cursor.fetchone()

def create_billing_view(page: Page):
    billing_manager = BillingManager()
    current_products = []

    def load_customers():
        customers = billing_manager.get_all_customers()
        customer_dropdown.options = [
            dropdown.Option(key=str(client['id']), text=client['nombre'])
            for client in customers
        ]
        page.update()

    def on_customer_change(e):
        if customer_dropdown.value:
            customer = billing_manager.get_customer_by_id(int(customer_dropdown.value))
            if customer:
                rut_field.value = customer['rfc']
                razon_social_field.value = customer['nombre']
                telefono_field.value = customer['telefono']
                comuna_field.value = customer['comuna']
                direccion_field.value = customer['direccion']
                ciudad_field.value = customer['ciudad']
                page.update()

    def calculate_totals():
        subtotal = sum(float(row['total']) for row in current_products)
        iva = subtotal * 0.19
        total = subtotal + iva
        
        total_neto_field.value = f"${subtotal:,.2f}"
        iva_field.value = f"${iva:,.2f}"
        total_field.value = f"${total:,.2f}"
        page.update()

    def add_product_to_table(e):
        dialog = AlertDialog(
            title=Text("Agregar Producto"),
            content=Column([
                TextField(label="Código", ref=lambda x: setattr(x, 'codigo', x)),
                TextField(label="Cantidad", ref=lambda x: setattr(x, 'cantidad', x)),
                TextField(label="Descripción", ref=lambda x: setattr(x, 'descripcion', x)),
                TextField(label="Precio Unitario", ref=lambda x: setattr(x, 'precio', x)),
            ]),
            actions=[
                TextButton("Cancelar", on_click=lambda e: close_dialog(e)),
                TextButton("Agregar", on_click=lambda e: save_product(e)),
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def save_product(e):
        try:
            dialog = page.dialog
            cantidad = float(dialog.content.controls[1].value)
            precio = float(dialog.content.controls[3].value)
            total = cantidad * precio
            
            new_product = {
                'codigo': dialog.content.controls[0].value,
                'cantidad': cantidad,
                'descripcion': dialog.content.controls[2].value,
                'precio': precio,
                'total': total
            }
            
            current_products.append(new_product)
            
            product_table.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(new_product['codigo'])),
                        DataCell(Text(str(new_product['cantidad']))),
                        DataCell(Text(new_product['descripcion'])),
                        DataCell(Text(f"${new_product['precio']:,.2f}")),
                        DataCell(Text(f"${new_product['total']:,.2f}")),
                    ]
                )
            )
            
            calculate_totals()
            close_dialog(e)
        except ValueError:
            # Handle invalid number input
            pass

    def clear_products(e):
        current_products.clear()
        product_table.rows.clear()
        calculate_totals()
        page.update()

    def close_dialog(e):
        page.dialog.open = False
        page.update()

    def generate_pdf(e):
        if not customer_dropdown.value or not current_products:
            page.show_snack_bar(SnackBar(content=Text("Por favor seleccione un cliente y agregue productos")))
            return

        try:
            # Create PDF
            pdf_path = "factura.pdf"
            c = canvas.Canvas(pdf_path, pagesize=letter)
            
            # Header
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 750, "FACTURA")
            c.setFont("Helvetica", 12)
            c.drawString(50, 730, f"Fecha: {datetime.now().strftime('%Y-%m-%d')}")
            
            # Customer info
            customer = billing_manager.get_customer_by_id(int(customer_dropdown.value))
            c.drawString(50, 700, f"Cliente: {customer['nombre']}")
            c.drawString(50, 680, f"RFC: {customer['rfc']}")
            c.drawString(50, 660, f"Dirección: {customer['direccion']}")
            
            # Products table
            y = 600
            c.drawString(50, y, "Código")
            c.drawString(150, y, "Cant.")
            c.drawString(200, y, "Descripción")
            c.drawString(350, y, "P.Unit")
            c.drawString(450, y, "Total")
            
            y -= 20
            for product in current_products:
                c.drawString(50, y, product['codigo'])
                c.drawString(150, y, str(product['cantidad']))
                c.drawString(200, y, product['descripcion'])
                c.drawString(350, y, f"${product['precio']:,.2f}")
                c.drawString(450, y, f"${product['total']:,.2f}")
                y -= 20
            
            # Totals
            subtotal = sum(float(row['total']) for row in current_products)
            iva = subtotal * 0.19
            total = subtotal + iva
            
            c.drawString(350, 200, f"Subtotal: ${subtotal:,.2f}")
            c.drawString(350, 180, f"IVA (19%): ${iva:,.2f}")
            c.drawString(350, 160, f"Total: ${total:,.2f}")
            
            c.save()
            
            # Open PDF
            os.startfile(pdf_path)
            
            page.show_snack_bar(SnackBar(content=Text("Factura generada exitosamente")))
        except Exception as ex:
            page.show_snack_bar(SnackBar(content=Text(f"Error al generar factura: {str(ex)}")))

    # Customer dropdown
    customer_dropdown = Dropdown(
        label="Seleccionar Cliente",
        width=300,
        on_change=on_customer_change
    )

    # Client details fields
    rut_field = TextField(label="RUT", width=300)
    razon_social_field = TextField(label="Razón Social", width=300)
    telefono_field = TextField(label="Teléfono", width=300)
    comuna_field = TextField(label="Comuna", width=300)
    direccion_field = TextField(label="Dirección", width=300)
    ciudad_field = TextField(label="Ciudad", width=300)

    # Client details
    client_details = Container(
        content=Container(
            content=Column([
                Row([
                    customer_dropdown,
                    rut_field,
                    razon_social_field,
                ]),
                Row([
                    telefono_field,
                    comuna_field,
                    TextField(
                        label="Fecha",
                        value=datetime.now().strftime("%Y-%m-%d"),
                        width=300,
                        disabled=True
                    ),
                ]),
                Row([
                    direccion_field,
                    ciudad_field,
                    TextField(label="Giro", width=300),
                ]),
            ]),
            bgcolor=Colors.PRIMARY_CONTAINER,
            padding=10,
            border_radius=10
        ),
        bgcolor=Colors.SURFACE_CONTAINER_HIGHEST,
        padding=20,
        border_radius=15
    )

    # Product table
    product_table = DataTable(
        columns=[
            DataColumn(Text("Código")),
            DataColumn(Text("Cantidad")),
            DataColumn(Text("Descripción")),
            DataColumn(Text("Precio Unitario")),
            DataColumn(Text("Total")),
        ],
        rows=[],
    )

    # Add product and clear buttons
    add_product_button = ElevatedButton(
        "Agregar Producto",
        icon=Icons.ADD,
        color=Colors.GREEN,
        on_click=add_product_to_table
    )
    
    clear_products_button = ElevatedButton(
        "Limpiar Productos",
        icon=Icons.CLEAR,
        color=Colors.ERROR,
        on_click=clear_products
    )
    
    generate_report_button = ElevatedButton(
        "Generar Factura",
        icon=Icons.TEXT_SNIPPET,
        on_click=generate_pdf
    )

    # Total fields
    observations_field = TextField(
        label="Observaciones",
        width=300 
    )
    total_neto_field = TextField(
        label="Total Neto", 
        value="0",
        width=300, 
        read_only=True
    )
    iva_field = TextField(
        label="IVA (19%)", 
        value="0",
        width=300, 
        read_only=True
    )
    total_field = TextField(
        label="Total", 
        value="0",
        width=300, 
        read_only=True
    )

    load_customers()

    return ListView(
        controls=[
            Container(
                content=Column(
                    controls=[
                        Text(
                            "Facturación",
                            theme_style=TextThemeStyle.HEADLINE_LARGE,
                            weight=FontWeight.BOLD
                        ),
                        Divider(),            
                        client_details,
                        product_table,
                        Column(
                            [
                                observations_field,
                                total_neto_field,
                                iva_field,
                                total_field
                            ]
                        ),
                        Row(
                            controls=[
                                add_product_button,
                                clear_products_button,
                                generate_report_button
                            ]
                        )
                    ],
                ),
                padding=20,
            )
        ],
        expand=True,
        spacing=10,
        padding=20,
    )