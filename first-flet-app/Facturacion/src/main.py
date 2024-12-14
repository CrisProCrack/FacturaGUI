import flet as ft
from flet import *
import billing
import billing_visualitation
import customers
import products

def create_login_view(page: Page, on_login_success):
    def on_register_success():
        page.controls.clear()
        page.add(create_login_view(page, on_login_success))
        page.update()
    def handle_login(e):
        # Add login validation logic here
        on_login_success()
    
    def go_to_register(e):
        page.controls.clear()
        page.add(create_register_view(page, on_register_success, on_login_success))
        page.update()

    headline = Text(
        "Inicio de Sesión", 
        theme_style=TextThemeStyle.HEADLINE_LARGE
    )
    usuario = TextField(
        label="Usuario", 
        width=300,
        prefix_icon=Icons.PERSON
    )
    contraseña = TextField(
        label="Contraseña", 
        password=True, 
        can_reveal_password=True, 
        width=300,
        prefix_icon=Icons.LOCK
    )
    registrate = TextButton(
        text="¿No tienes una cuenta? Registrate.",
        style=ButtonStyle(
            color={"": Colors.PINK_50}
        ),
        on_click=go_to_register
    )
    iniciar_sesion = FilledButton(
        text="Iniciar Sesión", 
        width=133, 
        height=40,
        on_click=handle_login
    )
    
    return Container(
        content=Card(
            content=Container(
                content=Column(
                    [headline, usuario, contraseña, registrate, iniciar_sesion],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                padding=20,
                width=477,
                height=360,
                alignment=alignment.center,
            ),
            elevation=2
        ),
        alignment=alignment.center,
        expand=True
    )

def create_register_view(page: Page, on_register_success, on_login_success):
    def handle_register(e):
        # Add registration logic here
        on_register_success()
    
    def go_to_login(e):
        page.controls.clear()
        page.add(create_login_view(page, on_login_success))
        page.update()

    headline = Text(
        "Registro de usuario", 
        theme_style=TextThemeStyle.HEADLINE_LARGE
    )
    usuario = TextField(
        label="Usuario", 
        width=300,
        prefix_icon=Icons.PERSON
    )
    contraseña = TextField(
        label="Contraseña", 
        password=True, 
        can_reveal_password=True, 
        width=300,
        prefix_icon=Icons.LOCK
    )
    contraseña_validate = TextField(
        label="Confirmar Contraseña", 
        password=True, 
        can_reveal_password=True, 
        width=300,
        prefix_icon=Icons.LOCK
    )
    correo = TextField(
        label="Correo",
        width=300,
        prefix_icon=Icons.EMAIL
    )
    telefono = TextField(
        label="Teléfono",
        width=300,
        prefix_icon=Icons.PHONE
    )
    label_iniciar_sesion = TextButton(
        text="¿Ya tienes una cuenta? Inicia sesión", 
        style=ButtonStyle(
            color={"": Colors.BLUE}
        ),
        on_click=go_to_login
    )
    registrar = FilledButton(
        text="Registrarse", 
        width=133, 
        height=40,
        on_click=handle_register
    )

    return Container(
        content=Card(
            content=Container(
                content=Column(
                    [
                        headline,
                        usuario,
                        contraseña,
                        contraseña_validate,
                        correo,
                        telefono,
                        label_iniciar_sesion,
                        registrar,
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                padding=20,
                width=477,
                height=572,
                alignment=alignment.center,
            ),
            elevation=2
        ),
        alignment=alignment.center,
        expand=True
    )

def main(page: ft.Page):
    def show_main_app():
        page.controls.clear()
        
        # Create instances of each view
        products_view = products.create_products_view(page)
        customers_view = customers.create_customers_view(page)
        billing_view = billing.create_billing_view(page)
        billing_visualization_view = billing_visualitation.create_billing_visualization_view(page)

        views = [products_view, customers_view, billing_view, billing_visualization_view]
        current_view = views[0]

        def change_nav(e):
            nonlocal current_view
            index = e.control.selected_index
            page.controls.pop()
            current_view = views[index]
            page.add(
                Row(
                    controls=[nav_rail, VerticalDivider(width=1), current_view],
                    expand=True,
                )
            )
            nav_rail.selected_index = index
            page.update()

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

        page.add(
            Row(
                controls=[nav_rail, VerticalDivider(width=1), current_view],
                expand=True,
            )
        )
        page.update()

    page.title = "Sistema de Facturación"
    page.padding = 0
    page.window.width = 1160
    page.window.height = 900
    page.theme_mode = ThemeMode.SYSTEM

    # Define themes
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

    # Start with login view
    page.add(create_login_view(page, show_main_app))

ft.app(target=main)