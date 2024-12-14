import flet as ft
from flet import *
import billing
import billing_visualitation
import customers
import products

def main(page: ft.Page):
    page.title = "Sistema de Facturación"
    page.padding = 0
    page.window.width = 1160
    page.window.height = 900
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

    # Create instances of each view
    products_view = products.create_products_view(page)
    customers_view = customers.create_customers_view(page)
    billing_view = billing.create_billing_view(page)
    billing_visualization_view = billing_visualitation.create_billing_visualization_view(page)

    # List of views to switch between
    views = [
        products_view,
        customers_view,
        billing_view,
        billing_visualization_view
    ]

    # Currently displayed view
    current_view = views[0]

    def change_nav(e):
        nonlocal current_view
        index = e.control.selected_index
        
        # Remove the current view
        page.controls.pop()
        
        # Add the new view
        current_view = views[index]
        page.add(
            Row(
                controls=[
                    nav_rail,
                    VerticalDivider(width=1),
                    current_view,      
                ],
                expand=True,
            )
        )
        
        # Update the navigation rail selection
        nav_rail.selected_index = index
        page.update()

    # Navigation rail
    nav_rail = NavigationRail(
        selected_index=0,
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

    # Initial view setup
    page.add(
        Row(
            controls=[
                nav_rail,
                VerticalDivider(width=1),
                current_view,      
            ],
            expand=True,
        )
    )

ft.app(target=main)