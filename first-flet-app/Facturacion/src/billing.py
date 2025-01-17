"""
Módulo de Facturación
--------------------
Sistema completo de facturación con generación de PDFs y gestión de inventario.

Clase BillingManager:
    Gestiona todas las operaciones de facturación.
    
    Métodos principales:
    - get_all_customers(): Lista clientes disponibles
    - get_customer_by_id(): Obtiene detalles de cliente
    - get_product_by_code(): Busca productos
    - update_product_quantity(): Actualiza inventario
    - create_invoice(): Crea nueva factura
    - get_invoice_details(): Obtiene detalles de factura
    - search_products(): Búsqueda dinámica de productos

Función create_billing_view:
    Crea la interfaz de facturación.
    
    Características:
    - Selección de cliente
    - Búsqueda de productos
    - Cálculo automático
    - Validación de stock
    - Generación de PDF
    - Gestión de observaciones
    
Funcionalidades:
    - Cálculo de IVA (19%)
    - Actualización automática de inventario
    - Validaciones en tiempo real
    - Generación de facturas en PDF
    - Sistema de observaciones
    - Búsqueda inteligente de productos
"""

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
        # Refrescar la conexión antes de obtener los datos
        self.conn = DatabaseConnection.get_connection()
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute("SELECT * FROM clientes")
        return self.cursor.fetchall()

    def get_customer_by_id(self, id):
        self.cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
        return self.cursor.fetchone()

    def get_product_by_code(self, code):
        # Refrescar la conexión antes de obtener los datos
        self.conn = DatabaseConnection.get_connection()
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute("SELECT * FROM productos WHERE codigo = %s", (code,))
        return self.cursor.fetchone()

    def update_product_quantity(self, product_id, quantity):
        self.cursor.execute("UPDATE productos SET cantidad = cantidad - %s WHERE id = %s", 
                          (quantity, product_id))
        self.conn.commit()

    def create_invoice(self, customer_id, total, products):
        try:
            # Insert into facturas
            self.cursor.execute(
                "INSERT INTO facturas (fecha, cliente_id, total) VALUES (%s, %s, %s)",
                (datetime.now().date(), customer_id, total)
            )
            factura_id = self.cursor.lastrowid

            # Insert invoice details
            for product in products:
                self.cursor.execute(
                    "INSERT INTO detalle_facturas (factura_id, producto_id, cantidad, precio_unitario, total) VALUES (%s, %s, %s, %s, %s)",
                    (factura_id, product['id'], product['cantidad'], product['precio'], product['total'])
                )
                # Update product quantity
                self.update_product_quantity(product['id'], product['cantidad'])

            self.conn.commit()
            return factura_id
        except Exception as e:
            self.conn.rollback()
            raise e

    def get_next_invoice_number(self):
        self.cursor.execute("SELECT MAX(id) as last_id FROM facturas")
        result = self.cursor.fetchone()
        return (result['last_id'] or 0) + 1

    def get_invoice_details(self, invoice_id):
        try:
            # Obtener información de la factura
            self.cursor.execute("""
                SELECT f.*, c.* 
                FROM facturas f 
                JOIN clientes c ON f.cliente_id = c.id 
                WHERE f.id = %s
            """, (invoice_id,))
            invoice = self.cursor.fetchone()

            # Obtener detalles de los productos
            self.cursor.execute("""
                SELECT df.*, p.codigo, p.descripcion 
                FROM detalle_facturas df 
                JOIN productos p ON df.producto_id = p.id 
                WHERE df.factura_id = %s
            """, (invoice_id,))
            details = self.cursor.fetchall()

            return invoice, details
        except Exception as e:
            print(f"Error getting invoice details: {e}")
            return None, None

    def get_all_invoices(self):
        try:
            self.cursor.execute("""
                SELECT f.*, c.nombre as cliente_nombre 
                FROM facturas f 
                JOIN clientes c ON f.cliente_id = c.id 
                ORDER BY f.fecha DESC
            """)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting invoices: {e}")
            return []

    def search_products(self, search_term):
        """Busca productos que coincidan con el término de búsqueda en código o nombre"""
        try:
            # Refrescar la conexión
            self.conn = DatabaseConnection.get_connection()
            self.cursor = self.conn.cursor(dictionary=True)
            
            query = """
                SELECT * FROM productos 
                WHERE codigo LIKE %s OR nombre LIKE %s OR descripcion LIKE %s
                LIMIT 10
            """
            search_pattern = f"%{search_term}%"
            self.cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error searching products: {e}")
            return []

def create_billing_view(page: Page):
    # Agregar esta constante al inicio de la función
    INVOICES_DIR = "facturas"
    # Crear la carpeta si no existe
    if not os.path.exists(INVOICES_DIR):
        os.makedirs(INVOICES_DIR)
    
    billing_manager = BillingManager()
    current_products = []

    # Obtener una instancia del administrador de clientes
    from customers import Customer
    customer_manager = Customer()
    
    def refresh_customers():
        # Actualizar la conexión antes de obtener los datos
        billing_manager.conn = DatabaseConnection.get_connection()
        billing_manager.cursor = billing_manager.conn.cursor(dictionary=True)
        customers = billing_manager.get_all_customers()
        customer_dropdown.options = [
            dropdown.Option(key=str(client['id']), text=client['nombre'])
            for client in customers
        ]
        page.update()

    # Registrar el observador para actualizar cuando haya cambios en clientes
    customer_manager.add_observer(refresh_customers)

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

    def refresh_data():
        # Función para actualizar todos los datos
        refresh_customers()
        page.update()

    def add_product_to_table(e):
        search_results = []
        selected_product = None

        def on_search_change(e):
            nonlocal search_results
            if len(e.control.value) >= 2:  # Buscar solo si hay al menos 2 caracteres
                search_results = billing_manager.search_products(e.control.value)
                # Actualizar las sugerencias
                search_suggestions.controls = [
                    ListTile(
                        title=Text(f"{product['codigo']} - {product['nombre']}"),
                        subtitle=Text(f"Stock: {product['cantidad']} - Precio: ${product['precio']:,.2f}"),
                        data=product,
                        on_click=lambda e: select_product(e.control.data)
                    )
                    for product in search_results
                ]
                search_suggestions.visible = True
            else:
                search_suggestions.controls = []
                search_suggestions.visible = False
            dialog.content.update()

        def select_product(product):
            nonlocal selected_product
            selected_product = product
            search_field.value = f"{product['codigo']} - {product['nombre']}"
            cantidad_field.value = "1"  # Valor por defecto
            search_suggestions.visible = False
            cantidad_field.visible = True
            availability_text.value = f"Stock disponible: {product['cantidad']}"
            availability_text.visible = True
            dialog.content.update()

        def save_selected_product(e):
            if not selected_product:
                page.show_snack_bar(SnackBar(content=Text("Por favor seleccione un producto")))
                return

            try:
                cantidad = float(cantidad_field.value)
                if cantidad > selected_product['cantidad']:
                    page.show_snack_bar(SnackBar(content=Text("Cantidad insuficiente en inventario")))
                    return

                new_product = {
                    'id': selected_product['id'],
                    'codigo': selected_product['codigo'],
                    'cantidad': cantidad,
                    'descripcion': selected_product['descripcion'],
                    'precio': float(selected_product['precio']),
                    'total': cantidad * float(selected_product['precio'])
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
            except ValueError as ex:
                page.show_snack_bar(SnackBar(content=Text(f"Error: {str(ex)}")))

        search_field = TextField(
            label="Buscar producto (código o nombre)",
            on_change=on_search_change,
            autofocus=True
        )

        search_suggestions = Column(
            controls=[],
            scroll=ScrollMode.AUTO,
            visible=False,
            height=200
        )

        cantidad_field = TextField(
            label="Cantidad",
            visible=False,
            keyboard_type=KeyboardType.NUMBER
        )

        availability_text = Text(
            "",
            visible=False
        )

        dialog = AlertDialog(
            title=Text("Agregar Producto"),
            content=Column([
                search_field,
                search_suggestions,
                cantidad_field,
                availability_text
            ]),
            actions=[
                TextButton("Cancelar", on_click=lambda e: close_dialog(e)),
                TextButton("Agregar", on_click=save_selected_product),
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

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
            customer_id = int(customer_dropdown.value)
            subtotal = sum(float(row['total']) for row in current_products)
            iva = subtotal * 0.19
            total = subtotal + iva

            # Create invoice in database
            invoice_id = billing_manager.create_invoice(customer_id, total, current_products)
            
            # Generate PDF with new path
            pdf_path = os.path.join(INVOICES_DIR, f"factura_{invoice_id}.pdf")
            c = canvas.Canvas(pdf_path, pagesize=letter)
            
            # Header
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 750, "FACTURA")
            c.drawString(450, 750, f"Folio: {invoice_id}")
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
            
            # Modificar la sección de totales para incluir observaciones
            y_totals = 200
            
            # Agregar observaciones si existen
            if observations_field.value:
                c.setFont("Helvetica-Bold", 10)
                c.drawString(50, y_totals + 40, "Observaciones:")
                c.setFont("Helvetica", 10)
                # Dividir las observaciones en líneas si son muy largas
                obs_words = observations_field.value.split()
                obs_lines = []
                current_line = []
                line_length = 0
                
                for word in obs_words:
                    if line_length + len(word) + 1 <= 80:  # 80 caracteres por línea aprox.
                        current_line.append(word)
                        line_length += len(word) + 1
                    else:
                        obs_lines.append(' '.join(current_line))
                        current_line = [word]
                        line_length = len(word)
                
                if current_line:
                    obs_lines.append(' '.join(current_line))
                
                # Dibujar cada línea de observaciones
                for i, line in enumerate(obs_lines):
                    c.drawString(50, y_totals + 20 - (i * 15), line)
                
                # Ajustar la posición de los totales
                y_totals -= (len(obs_lines) * 15 + 20)

            # Dibujar los totales
            c.setFont("Helvetica", 12)
            c.drawString(350, y_totals, f"Subtotal: ${subtotal:,.2f}")
            c.drawString(350, y_totals - 20, f"IVA (19%): ${iva:,.2f}")
            c.drawString(350, y_totals - 40, f"Total: ${total:,.2f}")
            
            c.save()
            
            # Open PDF
            os.startfile(pdf_path)
            
            # Clear products after successful invoice creation
            clear_products(None)
            
            page.show_snack_bar(SnackBar(content=Text("Factura generada exitosamente")))
        except Exception as ex:
            page.show_snack_bar(SnackBar(content=Text(f"Error al generar factura: {str(ex)}")))

    def on_route_change(e):
        # Actualizar datos cuando se regresa a la vista de facturación
        if page.route == "/billing":
            refresh_data()

    # Agregar manejador de cambio de ruta
    page.on_route_change = on_route_change

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

    # Asegurarse de que el dropdown se actualice inicialmente
    refresh_customers()

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