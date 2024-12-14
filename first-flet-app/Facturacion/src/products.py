import flet as ft
from flet import *

def create_products_view(page: Page):
    # Create a container for products view
    content_area = Container(
        content=Column(
            controls=[
                Text(
                    "Gestión de Productos",
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
                        ElevatedButton(
                            "Eliminar Producto",
                            icon=Icons.DELETE,
                            color=Colors.ERROR,
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

    return content_area

def open_add_product_dialog(e, page):
    add_product_dialog = AlertDialog(
        title=Text("Agregar Producto"),
        content=Column(
            controls=[
                TextField(label="Código"),
                TextField(label="Nombre"),
                TextField(label="Descripción"),
                TextField(label="Precio"),
                TextField(label="Cantidad"),
            ],
            tight=True,
        ),
        actions=[
            TextButton("Cancelar", on_click=lambda e: close_dialog(e, page)),
            TextButton("Guardar", on_click=lambda e: close_dialog(e, page)),
        ],
    )
    page.dialog = add_product_dialog
    add_product_dialog.open = True
    page.update()

def close_dialog(e, page):
    page.dialog.open = False
    page.update()

# Persistent table for products
products_table = DataTable(
    columns=[
        DataColumn(Text("ID")),
        DataColumn(Text("Código")),
        DataColumn(Text("Nombre")),
        DataColumn(Text("Descripción")),
        DataColumn(Text("Precio")),
        DataColumn(Text("Cantidad")),
    ],
    rows=[],
)