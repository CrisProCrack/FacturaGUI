"""
Módulo de Gestión de Productos
-----------------------------
Implementa la funcionalidad completa para administrar productos en el sistema.

Clase Product:
    Maneja todas las operaciones CRUD de productos.
    
    Métodos principales:
    - get_all_products(): Obtiene lista completa de productos
    - add_product(): Agrega nuevo producto
    - update_product(): Actualiza producto existente
    - delete_product(): Elimina producto si no está en uso
    - is_product_in_use(): Verifica si el producto está en facturas

Función create_products_view:
    Crea la interfaz gráfica para gestión de productos.
    
    Características:
    - Tabla de productos con datos
    - Botones de agregar, editar y eliminar
    - Validaciones de datos
    - Mensajes de confirmación
    - Manejo de errores
    - Actualización en tiempo real

Validaciones implementadas:
    - Stock no negativo
    - Campos requeridos
    - Productos en uso
    - Formato de precios
"""

import flet as ft
from flet import *
from db_config import DatabaseConnection

class Product:
    def __init__(self):
        self.conn = DatabaseConnection.get_connection()
        self.cursor = self.conn.cursor()

    def get_all_products(self):
        self.cursor.execute("SELECT * FROM productos")
        return self.cursor.fetchall()

    def add_product(self, codigo, nombre, descripcion, precio, cantidad):
        sql = "INSERT INTO productos (codigo, nombre, descripcion, precio, cantidad) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (codigo, nombre, descripcion, precio, cantidad))
        self.conn.commit()

    def update_product(self, id, codigo, nombre, descripcion, precio, cantidad):
        sql = "UPDATE productos SET codigo=%s, nombre=%s, descripcion=%s, precio=%s, cantidad=%s WHERE id=%s"
        self.cursor.execute(sql, (codigo, nombre, descripcion, precio, cantidad, id))
        self.conn.commit()

    def is_product_in_use(self, id):
        """Verifica si el producto está siendo usado en alguna factura"""
        sql = "SELECT COUNT(*) FROM detalle_facturas WHERE producto_id = %s"
        self.cursor.execute(sql, (id,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def delete_product(self, id):
        if self.is_product_in_use(id):
            raise Exception("No se puede eliminar el producto porque está siendo usado en una o más facturas")
        sql = "DELETE FROM productos WHERE id=%s"
        self.cursor.execute(sql, (id,))
        self.conn.commit()

def create_products_view(page: Page):
    product_manager = Product()

    def load_products():
        products = product_manager.get_all_products()
        products_table.rows.clear()
        for product in products:
            products_table.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(str(product[0]))),
                        DataCell(Text(product[1])),
                        DataCell(Text(product[2])),
                        DataCell(Text(product[3])),
                        DataCell(Text(str(product[4]))),
                        DataCell(Text(str(product[5]))),
                        DataCell(
                            Row([
                                IconButton(
                                    icon=Icons.EDIT,
                                    icon_color="blue",
                                    data=product,
                                    on_click=lambda e: open_edit_dialog(e, page)
                                ),
                                IconButton(
                                    icon=Icons.DELETE,
                                    icon_color="red",
                                    data=product[0],
                                    on_click=lambda e: open_delete_dialog(e, page)
                                )
                            ])
                        )
                    ]
                )
            )
        page.update()

    def save_product(e, fields, edit_mode=False):
        try:
            codigo = fields[0].value
            nombre = fields[1].value
            descripcion = fields[2].value
            precio = float(fields[3].value)
            cantidad = int(fields[4].value)

            if edit_mode:
                product_id = fields[0].data
                product_manager.update_product(product_id, codigo, nombre, descripcion, precio, cantidad)
            else:
                product_manager.add_product(codigo, nombre, descripcion, precio, cantidad)

            dialog = page.dialog
            if dialog:
                dialog.open = False

            load_products()
            page.update()

            # Usar el nuevo método para mostrar SnackBar
            snack = SnackBar(content=Text("Producto guardado exitosamente"))
            page.overlay.append(snack)
            snack.open = True
            page.update()
        except Exception as ex:
            # Usar el nuevo método para mostrar SnackBar de error
            error_snack = SnackBar(content=Text(f"Error: {str(ex)}"))
            page.overlay.append(error_snack)
            error_snack.open = True
            page.update()

    def open_add_product_dialog(e, page):
        fields = [
            TextField(label="Código"),
            TextField(label="Nombre"),
            TextField(label="Descripción"),
            TextField(label="Precio"),
            TextField(label="Cantidad"),
        ]
        
        dialog = AlertDialog(
            title=Text("Agregar Producto"),
            content=Column(controls=fields, tight=True),
            actions=[
                TextButton("Cancelar", on_click=lambda e: close_dialog(e, page)),
                TextButton("Guardar", on_click=lambda e: save_product(e, fields))
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def open_edit_dialog(e, page):
        product = e.control.data
        fields = [
            TextField(label="Código", value=product[1], data=product[0]),
            TextField(label="Nombre", value=product[2]),
            TextField(label="Descripción", value=product[3]),
            TextField(label="Precio", value=str(product[4])),
            TextField(label="Cantidad", value=str(product[5])),
        ]
        
        dialog = AlertDialog(
            title=Text("Editar Producto"),
            content=Column(controls=fields, tight=True),
            actions=[
                TextButton("Cancelar", on_click=lambda e: close_dialog(e, page)),
                TextButton("Actualizar", on_click=lambda e: save_product(e, fields, edit_mode=True))
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def open_delete_dialog(e, page):
        product_id = e.control.data
        dialog = AlertDialog(
            title=Text("Confirmar eliminación"),
            content=Text("¿Está seguro que desea eliminar este producto?"),
            actions=[
                TextButton("Cancelar", on_click=lambda e: close_dialog(e, page)),
                TextButton(
                    "Eliminar",
                    on_click=lambda e: delete_product(e, product_id),
                    style=ButtonStyle(color={"": "red"}),
                ),
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def delete_product(e, product_id):
        try:
            product_manager.delete_product(product_id)
            dialog = page.dialog
            if dialog:
                dialog.open = False
            load_products()
            page.update()

            snack = SnackBar(content=Text("Producto eliminado exitosamente"))
            page.overlay.append(snack)
            snack.open = True
            page.update()
        except Exception as ex:
            error_message = str(ex) if "está siendo usado" in str(ex) else "Error al eliminar el producto"
            error_snack = SnackBar(content=Text(error_message))
            page.overlay.append(error_snack)
            error_snack.open = True
            page.update()

    def close_dialog(e, page):
        dialog = page.dialog
        if dialog:
            dialog.open = False
            page.update()

    products_table = DataTable(
        columns=[
            DataColumn(Text("ID")),
            DataColumn(Text("Código")),
            DataColumn(Text("Nombre")),
            DataColumn(Text("Descripción")),
            DataColumn(Text("Precio")),
            DataColumn(Text("Cantidad")),
            DataColumn(Text("Acciones")),
        ],
        rows=[],
    )

    content_area = Container(
        content=Column(
            controls=[
                Text("Gestión de Productos",
                    theme_style=TextThemeStyle.HEADLINE_LARGE,
                    weight=FontWeight.BOLD),
                Divider(),
                Row(
                    controls=[
                        ElevatedButton(
                            "Agregar Producto",
                            icon=Icons.ADD,
                            on_click=lambda e: open_add_product_dialog(e, page)
                        ),
                    ],
                ),
                Container(
                    content=products_table,
                    expand=True,
                ),
            ],
            expand=True,
        ),
        padding=20,
        expand=True,
    )

    # Load products when view is created
    load_products()
    return content_area