"""
Módulo de Gestión de Clientes
----------------------------
Implementa el manejo completo de clientes utilizando el patrón Singleton y Observer.

Clase Customer:
    Singleton que gestiona las operaciones de clientes.
    
    Características:
    - Patrón Singleton para instancia única
    - Sistema de observadores para actualizaciones
    - Operaciones CRUD completas
    
    Métodos principales:
    - add_observer(): Registra observadores
    - notify_observers(): Notifica cambios
    - get_all_customers(): Lista todos los clientes
    - add_customer(): Agrega nuevo cliente
    - update_customer(): Actualiza cliente
    - delete_customer(): Elimina cliente

Función create_customers_view:
    Crea la interfaz de usuario para gestión de clientes.
    
    Características:
    - Tabla de clientes
    - Formularios de edición
    - Validaciones en tiempo real
    - Mensajes de estado
    - Actualización automática
    
Campos del cliente:
    - Nombre
    - Correo
    - Teléfono
    - Dirección
    - Comuna
    - Ciudad
    - RFC
"""

import flet as ft
from flet import *
from db_config import DatabaseConnection

class Customer:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Customer, cls).__new__(cls)
            cls._instance.observers = []
            cls._instance.conn = DatabaseConnection.get_connection()
            cls._instance.cursor = cls._instance.conn.cursor()
        return cls._instance

    def __init__(self):
        # El constructor no necesita hacer nada más
        pass

    def add_observer(self, callback):
        self.observers.append(callback)

    def notify_observers(self):
        for callback in self.observers:
            callback()

    def get_all_customers(self):
        self.cursor.execute("SELECT * FROM clientes")
        return self.cursor.fetchall()

    def add_customer(self, nombre, correo, telefono, direccion, comuna, ciudad, rfc):
        try:
            sql = "INSERT INTO clientes (nombre, correo, telefono, direccion, comuna, ciudad, rfc) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (nombre, correo, telefono, direccion, comuna, ciudad, rfc))
            self.conn.commit()
            self.notify_observers()  # Notificar cambios
        except Exception as e:
            self.conn.rollback()
            raise e

    def update_customer(self, id, nombre, correo, telefono, direccion, comuna, ciudad, rfc):
        try:
            sql = "UPDATE clientes SET nombre=%s, correo=%s, telefono=%s, direccion=%s, comuna=%s, ciudad=%s, rfc=%s WHERE id=%s"
            self.cursor.execute(sql, (nombre, correo, telefono, direccion, comuna, ciudad, rfc, id))
            self.conn.commit()
            self.notify_observers()  # Notificar cambios
        except Exception as e:
            self.conn.rollback()
            raise e

    def delete_customer(self, id):
        try:
            sql = "DELETE FROM clientes WHERE id=%s"
            self.cursor.execute(sql, (id,))
            self.conn.commit()
            self.notify_observers()  # Notificar cambios
        except Exception as e:
            self.conn.rollback()
            raise e

def create_customers_view(page: Page):
    customer_manager = Customer()

    def load_customers():
        customers = customer_manager.get_all_customers()
        customers_table.rows.clear()
        for customer in customers:
            customers_table.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(str(customer[0]))),  # ID
                        DataCell(Text(customer[1])),       # Nombre
                        DataCell(Text(customer[2] or "")), # Correo
                        DataCell(Text(customer[3] or "")), # Teléfono
                        DataCell(Text(customer[4] or "")), # Dirección
                        DataCell(Text(customer[5] or "")), # Comuna
                        DataCell(Text(customer[6] or "")), # Ciudad
                        DataCell(Text(customer[7] or "")), # RFC
                        DataCell(
                            Row([
                                IconButton(
                                    icon=Icons.EDIT,
                                    icon_color="blue",
                                    data=customer,
                                    on_click=lambda e: open_edit_dialog(e, page)
                                ),
                                IconButton(
                                    icon=Icons.DELETE,
                                    icon_color="red",
                                    data=customer[0],
                                    on_click=lambda e: open_delete_dialog(e, page)
                                )
                            ])
                        )
                    ]
                )
            )
        page.update()

    def save_customer(e, fields, edit_mode=False):
        try:
            nombre = fields[0].value
            correo = fields[1].value
            telefono = fields[2].value
            direccion = fields[3].value
            comuna = fields[4].value
            ciudad = fields[5].value
            rfc = fields[6].value

            if edit_mode:
                customer_id = fields[0].data
                customer_manager.update_customer(customer_id, nombre, correo, telefono, direccion, comuna, ciudad, rfc)
            else:
                customer_manager.add_customer(nombre, correo, telefono, direccion, comuna, ciudad, rfc)

            dialog = page.dialog
            if (dialog):
                dialog.open = False

            load_customers()
            page.update()

            snack = SnackBar(content=Text("Cliente guardado exitosamente"))
            page.overlay.append(snack)
            snack.open = True
            page.update()
        except Exception as ex:
            error_snack = SnackBar(content=Text(f"Error: {str(ex)}"))
            page.overlay.append(error_snack)
            error_snack.open = True
            page.update()

    def open_add_client_dialog(e, page):
        fields = [
            TextField(label="Nombre"),
            TextField(label="Correo"),
            TextField(label="Teléfono"),
            TextField(label="Dirección"),
            TextField(label="Comuna"),
            TextField(label="Ciudad"),
            TextField(label="RFC"),
        ]
        
        dialog = AlertDialog(
            title=Text("Agregar Cliente"),
            content=Column(controls=fields, tight=True),
            actions=[
                TextButton("Cancelar", on_click=lambda e: close_dialog(e, page)),
                TextButton("Guardar", on_click=lambda e: save_customer(e, fields))
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def open_edit_dialog(e, page):
        customer = e.control.data
        fields = [
            TextField(label="Nombre", value=customer[1], data=customer[0]),
            TextField(label="Correo", value=customer[2] or ""),
            TextField(label="Teléfono", value=customer[3] or ""),
            TextField(label="Dirección", value=customer[4] or ""),
            TextField(label="Comuna", value=customer[5] or ""),
            TextField(label="Ciudad", value=customer[6] or ""),
            TextField(label="RFC", value=customer[7] or ""),
        ]
        
        dialog = AlertDialog(
            title=Text("Editar Cliente"),
            content=Column(controls=fields, tight=True),
            actions=[
                TextButton("Cancelar", on_click=lambda e: close_dialog(e, page)),
                TextButton("Actualizar", on_click=lambda e: save_customer(e, fields, edit_mode=True))
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def open_delete_dialog(e, page):
        customer_id = e.control.data
        dialog = AlertDialog(
            title=Text("Confirmar eliminación"),
            content=Text("¿Está seguro que desea eliminar este cliente?"),
            actions=[
                TextButton("Cancelar", on_click=lambda e: close_dialog(e, page)),
                TextButton(
                    "Eliminar",
                    on_click=lambda e: delete_customer(e, customer_id),
                    style=ButtonStyle(color={"": "red"}),
                ),
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def delete_customer(e, customer_id):
        try:
            customer_manager.delete_customer(customer_id)
            dialog = page.dialog
            if dialog:
                dialog.open = False
            load_customers()
            page.update()

            snack = SnackBar(content=Text("Cliente eliminado exitosamente"))
            page.overlay.append(snack)
            snack.open = True
            page.update()
        except Exception as ex:
            error_snack = SnackBar(content=Text(f"Error al eliminar: {str(ex)}"))
            page.overlay.append(error_snack)
            error_snack.open = True
            page.update()

    def close_dialog(e, page):
        dialog = page.dialog
        if dialog:
            dialog.open = False
            page.update()

    customers_table = DataTable(
        columns=[
            DataColumn(Text("ID")),
            DataColumn(Text("Nombre")),
            DataColumn(Text("Correo")),
            DataColumn(Text("Teléfono")),
            DataColumn(Text("Dirección")),
            DataColumn(Text("Comuna")),
            DataColumn(Text("Ciudad")),
            DataColumn(Text("RFC")),
            DataColumn(Text("Acciones")),
        ],
        rows=[],
    )

    content_area = Container(
        content=Column(
            controls=[
                Text("Gestión de Clientes",
                    theme_style=TextThemeStyle.HEADLINE_LARGE,
                    weight=FontWeight.BOLD),
                Divider(),
                Row(
                    controls=[
                        ElevatedButton(
                            "Agregar Cliente",
                            icon=Icons.ADD,
                            on_click=lambda e: open_add_client_dialog(e, page)
                        ),
                    ],
                ),
                Container(
                    content=customers_table,
                    expand=True,
                ),
            ],
            expand=True,
        ),
        padding=20,
        expand=True,
    )

    # Load customers when view is created
    load_customers()
    return content_area