import flet as ft
from flet import *

def main(page: Page):
    page.title = "Sistema de Facturación"
    page.padding = 0
    # Fix window dimension deprecations
    page.window.width = 905
    page.window.height = 680
    page.theme_mode = ThemeMode.SYSTEM

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

    def open_add_product_dialog(e):
        page.dialog = add_product_dialog
        add_product_dialog.open = True
        page.update()

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
            TextButton("Cancelar", on_click=lambda e: close_dialog(e)),
            TextButton("Guardar", on_click=lambda e: close_dialog(e)),
        ],
    )

    def close_dialog(e):
        add_product_dialog.open = False
        page.update()

    nav_rail = NavigationRail(
        selected_index=1,
        label_type=NavigationRailLabelType.ALL,
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

    products_table = DataTable(
        columns=[
            DataColumn(Text("ID")),
            DataColumn(Text("Nonbre")),
            DataColumn(Text("Correo")),
            DataColumn(Text("Teléfono")),
            DataColumn(Text("RFC")),
            DataColumn(Text("Dirección")),
            DataColumn(Text("Comuna")),
            DataColumn(Text("Ciudad"))
        ],
        rows=[],
    )

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
                            on_click=open_add_product_dialog
                        ),
                        ElevatedButton(
                            "Eliminar Cliente",
                            icon=Icons.DELETE,
                            color=Colors.ERROR,
                        ),
                    ],
                ),
                Container(
                    content=products_table,
                    expand=True,  # Expande la tabla para ocupar espacio disponible
                ),
            ],
            expand=True,  # Permite que el contenido ocupe espacio dinámicamente
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

app(target=main)