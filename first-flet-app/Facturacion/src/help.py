import flet as ft
from flet import *

def create_help_view(page: Page):
    help_sections = [
        {
            "title": "Facturación - Guía Detallada",
            "content": [
                "• Para crear una nueva factura:",
                "  1. Seleccione un cliente del menú desplegable",
                "  2. Los datos del cliente se cargarán automáticamente",
                "  3. Use el botón 'Agregar Producto' para buscar productos",
                "  4. Puede buscar productos por código o nombre",
                "  5. Ingrese la cantidad deseada del producto",
                "  6. El sistema validará automáticamente el stock disponible",
                "  7. Los totales se calculan automáticamente",
                "",
                "• Campos importantes:",
                "  - Observaciones: Para notas adicionales en la factura",
                "  - Total Neto: Monto sin IVA",
                "  - IVA: 19% del total neto",
                "  - Total: Monto final con IVA",
                "",
                "• Funciones adicionales:",
                "  - Botón 'Limpiar Productos': Elimina todos los productos agregados",
                "  - Botón 'Generar Factura': Crea el PDF y guarda la factura",
                "  - Los productos se descuentan automáticamente del inventario",
                "  - Las facturas generadas se pueden reimprimir desde la sección 'Reimpresión'"
            ]
        },
        {
            "title": "Productos",
            "content": [
                "• Gestión completa de productos del inventario",
                "• Agregar nuevos productos con código, nombre, descripción, precio y cantidad",
                "• Editar productos existentes",
                "• Eliminar productos (si no están en uso en facturas)",
                "• Vista en tabla con todos los productos",
                "• Validación de stock y datos"
            ]
        },
        {
            "title": "Clientes",
            "content": [
                "• Administración de información de clientes",
                "• Registro de nuevos clientes con datos completos",
                "• Editar información de clientes existentes",
                "• Eliminar registros de clientes",
                "• Campos incluyen: nombre, correo, teléfono, dirección, comuna, ciudad y RFC",
                "• Vista en tabla de todos los clientes"
            ]
        },
        {
            "title": "Facturación",
            "content": [
                "• Creación de nuevas facturas",
                "• Selección de cliente desde el catálogo",
                "• Búsqueda y agregado de productos",
                "• Cálculo automático de totales e IVA",
                "• Validación de stock disponible",
                "• Generación de PDF de la factura",
                "• Campo para observaciones",
                "• Los productos seleccionados actualizan automáticamente el inventario"
            ]
        },
        {
            "title": "Reimpresión de Facturas",
            "content": [
                "• Visualización del historial de facturas",
                "• Búsqueda de facturas por número",
                "• Ver detalles de facturas anteriores",
                "• Reimpresión de facturas en PDF",
                "• Muestra fecha, cliente y monto total"
            ]
        }
    ]

    sections = []
    for section in help_sections:
        content_items = [Text(item, 
                            size=14,
                            weight=FontWeight.W_400) 
                        for item in section["content"]]
        
        section_card = Card(
            content=Container(
                content=Column([
                    Text(
                        section["title"],
                        style=TextThemeStyle.TITLE_LARGE,
                        weight=FontWeight.BOLD,
                        color=colors.PRIMARY
                    ),
                    Divider(thickness=0.5),
                    Column(content_items, spacing=10)
                ]),
                padding=20
            ),
            elevation=2,
            margin=margin.only(bottom=20)
        )
        sections.append(section_card)

    return Container(
        content=Column(
            controls=[
                Container(
                    content=Text(
                        "Ayuda del Sistema",
                        style=TextThemeStyle.HEADLINE_LARGE,
                        weight=FontWeight.BOLD,
                    ),
                    padding=padding.only(bottom=10)
                ),
                Divider(height=2),
                Container(
                    content=ListView(
                        controls=sections,
                        spacing=10,
                        padding=padding.only(right=20),
                    ),
                    expand=True,
                )
            ],
            scroll=ScrollMode.AUTO,
            expand=True,
        ),
        padding=padding.all(20),
        expand=True,
    )
