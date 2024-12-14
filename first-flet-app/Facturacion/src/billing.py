import flet as ft
from flet import *
from datetime import datetime

def create_billing_view(page: Page):
    # Simulated clients
    clients = [
        {"nombre": "Cliente 1", "rut": "12345678-9", "razon_social": "Empresa 1", 
         "telefono": "912345678", "comuna": "Santiago", "direccion": "Calle 123",
         "ciudad": "Santiago", "giro": "Comercio"}
    ]

    # Customers dropdown
    customer_dropdown = Dropdown(
        label="Seleccionar Cliente",
        width=300,
        options=[
            dropdown.Option(client["nombre"]) for client in clients
        ]
    )

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
        on_click=lambda e: print("Agregar Producto")
    )
    
    clear_products_button = ElevatedButton(
        "Limpiar Productos",
        icon=Icons.CLEAR,
        color=Colors.ERROR,
        on_click=lambda e: print("Limpiar Productos")
    )
    
    generate_report_button = ElevatedButton(
        "Generar Reporte",
        icon=Icons.TEXT_SNIPPET,
        on_click=lambda e: print("Generar Reporte (PDF)")
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