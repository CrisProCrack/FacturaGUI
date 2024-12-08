import flet as ft
from flet import *
from datetime import datetime

def main(page: Page):
    page.title = "Sistema de Facturación"
    page.padding = 0
    # Fix window dimension deprecations
    page.window.width = 1160
    page.window.height = 900
    page.theme_mode = ThemeMode.SYSTEM

    # Define themes for light and dark modes
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

    # Navigation rail
    nav_rail = NavigationRail(
        selected_index=0,
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

    # Table
    product_table = DataTable(
        columns=[
            DataColumn(Text("Código")),
            DataColumn(Text("Cantidad")),
            DataColumn(Text("Descripción")),
            DataColumn(Text("Precio Unitario")),
            DataColumn(Text("Total")),
        ],

        rows=[],  # Se agregan las filas en la siguiente sección
    )

    # Botoón para agregar productos
    add_product_button = ElevatedButton(
        "Agregar Producto",
        icon=Icons.ADD,
        on_click=lambda e: print("Agregar Producto")
        )
    # Botón para limpiar productos
    clear_products_button = ElevatedButton(
        "Limpiar Productos",
        icon=Icons.CLEAR,
        on_click=lambda e: print("Limpiar Productos")
        )
    # Boton para generar reportes
    generate_report_button = ElevatedButton(
        "Generar Reporte",
        icon=Icons.TEXT_SNIPPET,
        on_click=lambda e: print("Generar Reporte (PDF)")
        )

    #Simulated clients
    clients = [
        {"nombre": "Cliente 1", "rut": "12345678-9", "razon_social": "Empresa 1", 
         "telefono": "912345678", "comuna": "Santiago", "direccion": "Calle 123",
         "ciudad": "Santiago", "giro": "Comercio"}
    ]
    # Customers labels
    customer_dropdown = Dropdown(
        label="Seleccionar Cliente",
        width=300,
        options=[
            dropdown.Option(clients["nombre"]) for clients in clients
        ]
    )

    #Campos totales
    observations_field = TextField(
        label="Observaciones",
        width=300 
        )
    total_neto_field = TextField(
        label="Total Neto", 
        value="0",
        width=300, 
        read_only=True)
    iva_field = TextField(
        label="IVA (19%)", 
        value="0",
        width=300, 
        read_only=True)
    total_field = TextField(
        label="Total", 
        value="0",
        width=300, 
        read_only=True)

    # Client details
    client_details = Container(
    content=Container(
        content=Column([
            Row([
                customer_dropdown,
                TextField(label="RUT", width=300),
                TextField(label="Razón Social", width=300),
            ]),
            Row([
                TextField(label="Teléfono", width=300),
                TextField(label="Comuna", width=300),
                TextField(
                    label="Fecha",
                    value=datetime.now().strftime("%Y-%m-%d"),
                    width=300,
                    disabled=True
                ),
            ]),
            Row([
                TextField(label="Dirección", width=300),
                TextField(label="Ciudad", width=300),
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

    content_area = Container(
        content=Column(
            controls=[
                # Titulo
                Text(
                    "Facturación",
                    theme_style=TextThemeStyle.HEADLINE_LARGE,
                    weight=FontWeight.BOLD
                ),
                Divider(),            
                #Parte de la tabla
                Container(
                    content=client_details,
                ),
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