import flet as ft
from flet import *

def main(page: Page):
    page.title = "Inicio de Sesión"
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

    
    # Creación de los componentes
    headline = Text(
        "Inicio de Sesión", 
        theme_style=TextThemeStyle.HEADLINE_LARGE  # Fix text style deprecation
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
    # Fix colors deprecation
    registrate = Text(
        "¿No tienes una cuenta? Registrate.", 
        theme_style=TextThemeStyle.BODY_MEDIUM, 
        color=Colors.PINK_50  # Updated from colors to Colors
        )
    iniciar_sesion = FilledButton(
        text="Iniciar Sesión", 
        width=133, 
        height=40
        )
    
    # Crear una tarjeta que contenga todos los componentes
    card = Card(
        content=Container(
            content=Column(
                [
                    headline,
                    usuario,
                    contraseña,
                    registrate,
                    iniciar_sesion,
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=20,
            width=477,  # Updated width
            height=360,  # Updated height
            alignment=alignment.center,
        ),
        elevation=2
    )

    # Add container to center the card
    page.add(
        Container(
            content=card,
            alignment=alignment.center,
            expand=True
        )
    )

ft.app(target=main)