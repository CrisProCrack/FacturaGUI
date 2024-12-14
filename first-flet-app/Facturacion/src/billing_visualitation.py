import flet as ft
from flet import *

def create_billing_visualization_view(page: ft.Page):
    # Botón de visualizar factura
    btn_view_bill = ElevatedButton(
        "Visualizar Factura",
        icon=Icons.DESCRIPTION,
        on_click=lambda e: print("Visualizar factura"),
    )

    #Tabla de facturas
    billing_table = DataTable(
        columns=[
            DataColumn(Text("Número")),
            DataColumn(Text("Fecha")),
            DataColumn(Text("Cliente")),
            DataColumn(Text("Total")),
        ],
        rows=[
        ],
    )

    # Contenido de la página
    content_area = Container(
        content=Column(
            controls=[
                # Titulo
                Text(
                    "Ver Facturas",
                    theme_style=TextThemeStyle.HEADLINE_LARGE,
                    weight=FontWeight.BOLD
                ),
                Divider(),            
                #Parte de la tabla
                Row(
                controls=[billing_table],
                alignment=MainAxisAlignment.CENTER,
                spacing=20
                ),
                Divider(),
                #Botón de visualizar factura
                Row(
                controls=[btn_view_bill],
                alignment=MainAxisAlignment.CENTER,
                spacing=20
                ),
            ],
            expand=True,
        ),
        padding=20,
        expand=True,
    )

    return content_area