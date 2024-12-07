import flet as ft
from flet import TextField, ElevatedButton, Text, Column, Container, View, Page

def main(page: ft.Page):
    # Configuración básica de la página
    page.title = "Sistema de Login"
    page.window_width = 400
    page.window_height = 600
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    
    # Configuración del tema (corregida)
    page.theme_mode = "light"
    page.padding = 20
    page.bgcolor = ft.colors.WHITE

    # Vista de Login
    def login_view():
        username = TextField(
            label="Usuario",
            width=300,
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE_700
        )
        password = TextField(
            label="Contraseña",
            password=True,
            width=300,
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE_700
        )
        
        def handle_login(e):
            if not username.value or not password.value:
                page.show_snack_bar(
                    ft.SnackBar(content=Text("Por favor complete todos los campos"))
                )
                return
            page.show_snack_bar(
                ft.SnackBar(content=Text("Iniciando sesión..."))
            )

        login_container = Container(
            content=Column(
                controls=[
                    Text(
                        "Iniciar Sesión",
                        size=30,
                        weight="bold",
                        color=ft.colors.BLUE_700
                    ),
                    username,
                    password,
                    ElevatedButton(
                        "Ingresar",
                        width=300,
                        on_click=handle_login,
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE_700
                        )
                    ),
                    ElevatedButton(
                        "Registrarse",
                        width=300,
                        on_click=lambda _: page.go("/register"),
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE_400
                        )
                    ),
                    ElevatedButton(
                        "¿Olvidaste tu contraseña?",
                        width=300,
                        on_click=lambda _: page.go("/recovery"),
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE_400
                        )
                    ),
                ],
                horizontal_alignment="center",
                spacing=20,
            ),
            padding=40,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_GREY_100,
            )
        )
        return View("/login", [login_container])

    # Vista de Registro
    def register_view():
        username = TextField(
            label="Usuario",
            width=300,
            border_color=ft.colors.BLUE_400
        )
        email = TextField(
            label="Correo electrónico",
            width=300,
            border_color=ft.colors.BLUE_400
        )
        password = TextField(
            label="Contraseña",
            password=True,
            width=300,
            border_color=ft.colors.BLUE_400
        )
        confirm_password = TextField(
            label="Confirmar contraseña",
            password=True,
            width=300,
            border_color=ft.colors.BLUE_400
        )

        def handle_register(e):
            if not all([username.value, email.value, password.value, confirm_password.value]):
                page.show_snack_bar(
                    ft.SnackBar(content=Text("Por favor complete todos los campos"))
                )
                return
            if password.value != confirm_password.value:
                page.show_snack_bar(
                    ft.SnackBar(content=Text("Las contraseñas no coinciden"))
                )
                return
            page.show_snack_bar(
                ft.SnackBar(content=Text("Registrando usuario..."))
            )

        register_container = Container(
            content=Column(
                controls=[
                    Text(
                        "Registro de Usuario",
                        size=30,
                        weight="bold",
                        color=ft.colors.BLUE_700
                    ),
                    username,
                    email,
                    password,
                    confirm_password,
                    ElevatedButton(
                        "Registrar",
                        width=300,
                        on_click=handle_register,
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE_700
                        )
                    ),
                    ElevatedButton(
                        "Volver",
                        width=300,
                        on_click=lambda _: page.go("/login"),
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE_400
                        )
                    ),
                ],
                horizontal_alignment="center",
                spacing=20,
            ),
            padding=40,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_GREY_100,
            )
        )
        return View("/register", [register_container])

    # Vista de Recuperación de Contraseña
    def recovery_view():
        email = TextField(
            label="Correo electrónico",
            width=300,
            border_color=ft.colors.BLUE_400
        )

        def handle_recovery(e):
            if not email.value:
                page.show_snack_bar(
                    ft.SnackBar(content=Text("Por favor ingrese su correo electrónico"))
                )
                return
            page.show_snack_bar(
                ft.SnackBar(content=Text("Enviando instrucciones de recuperación..."))
            )

        recovery_container = Container(
            content=Column(
                controls=[
                    Text(
                        "Recuperar Contraseña",
                        size=30,
                        weight="bold",
                        color=ft.colors.BLUE_700
                    ),
                    email,
                    ElevatedButton(
                        "Recuperar",
                        width=300,
                        on_click=handle_recovery,
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE_700
                        )
                    ),
                    ElevatedButton(
                        "Volver",
                        width=300,
                        on_click=lambda _: page.go("/login"),
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE_400
                        )
                    ),
                ],
                horizontal_alignment="center",
                spacing=20,
            ),
            padding=40,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_GREY_100,
            )
        )
        return View("/recovery", [recovery_container])

    # Configurar las rutas
    page.views.append(login_view())
    page.views.append(register_view()) 
    page.views.append(recovery_view())

    # Iniciar en la vista de login
    page.go("/login")

if __name__ == "__main__":
    ft.app(target=main)