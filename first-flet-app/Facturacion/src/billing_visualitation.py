import flet as ft
from flet import *

def main(page: ft.Page):
    page.title = "Sistema de Facturación"
    page.window.width = 1000
    page.window.height = 800
    page.theme_mode = ft.ThemeMode.SYSTEM

    # Define themes for light and dark modes
    page.theme = Theme(
        color_scheme_seed=Colors.PINK,
        color_scheme=ColorScheme(
            primary=Colors.PINK_400,
            secondary=Colors.PINK_200,
            surface_tint=Colors.PINK_100,
            background=Colors.PINK_50,

        )
    )
    
    page.dark_theme = Theme(
        color_scheme_seed=Colors.PINK,
        color_scheme=ColorScheme(
            primary=Colors.PINK_200,
            secondary=Colors.PINK_400,
            surface_tint=Colors.PINK_700,
            background=Colors.PINK_800,
        )
    )

    def change_nav(e):
        index = e.control.selected_index
        nav_rail.selected_index = index
        page.update()

    # Botón de visulizar factura
    btn_view_bill = ElevatedButton(
        "Visualizar Factura",
        icon=Icons.DESCRIPTION,
        on_click=lambda e: print("Visualizar factura"),
    )

    # Navigation rail
    nav_rail = NavigationRail(
        selected_index=3,
        label_type= NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        destinations=[
            NavigationRailDestination(
                icon=Icons.INVENTORY,
                selected_icon=Icons.INVENTORY,
                label="Productos",
            ),
            NavigationRailDestination(
                icon=Icons.PEOPLE,
                selected_icon=Icons.PEOPLE,
                label="Clientes",
            ),
            NavigationRailDestination(
                icon=Icons.RECEIPT_LONG,
                selected_icon=Icons.RECEIPT_LONG,
                label="Facturación",
            ),
            NavigationRailDestination(
                icon=Icons.DESCRIPTION,
                selected_icon=Icons.DESCRIPTION,
                label="Ver Facturas",
            ),
        ],
        on_change=change_nav,
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

    page.add(
        Row(
            controls=[
                nav_rail,
                VerticalDivider(width=1),
                content_area,      
                ],
            expand=True,  # Hace que la fila principal ocupe toda la pantalla
        )
    )

app (target=main)
