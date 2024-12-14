import flet as ft
from flet import *

def create_customers_view(page: Page):
    content_area = Container(
        content=Column(
            controls=[
                Text(
                    "Gestión de Clientes",
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
                        ElevatedButton(
                            "Eliminar Cliente",
                            icon=Icons.DELETE,
                            color=Colors.ERROR,
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

    return content_area

def open_add_client_dialog(e, page):
    add_client_dialog = AlertDialog(
        title=Text("Agregar Cliente"),
        content=Column(
            controls=[
                TextField(label="Nombre"),
                TextField(label="Correo"),
                TextField(label="Teléfono"),
                TextField(label="RFC"),
                TextField(label="Dirección"),
                TextField(label="Comuna"),
                TextField(label="Ciudad"),
            ],
            tight=True,
        ),
        actions=[
            TextButton("Cancelar", on_click=lambda e: close_dialog(e, page)),
            TextButton("Guardar", on_click=lambda e: close_dialog(e, page)),
        ],
    )
    page.dialog = add_client_dialog
    add_client_dialog.open = True
    page.update()

def close_dialog(e, page):
    page.dialog.open = False
    page.update()

# Persistent table for customers
customers_table = DataTable(
    columns=[
        DataColumn(Text("ID")),
        DataColumn(Text("Nombre")),
        DataColumn(Text("Correo")),
        DataColumn(Text("Teléfono")),
        DataColumn(Text("RFC")),
        DataColumn(Text("Dirección")),
        DataColumn(Text("Comuna")),
        DataColumn(Text("Ciudad"))
    ],
    rows=[],
)