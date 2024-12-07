import flet as ft

def main(page: ft.Page):
    page.title = "Interfaz de Inicio de Sesión"
    page.window_width = 400
    page.window_height = 600
    page.theme = ft.Theme(
        primary_color=ft.colors.BLUE,
        secondary_color=ft.colors.LIGHT_BLUE,
        background_color=ft.colors.WHITE,
        surface_color=ft.colors.WHITE,
        error_color=ft.colors.RED,
        primary_text_color=ft.colors.BLACK,
        secondary_text_color=ft.colors.GREY,
    )

    def iniciar_sesion(e):
        print("Iniciar sesión")

    def registrar_usuario(e):
        print("Registrar usuario")

    def recuperar_contrasena(e):
        print("Recuperar contraseña")

    # Crear los campos de texto y botones
    usuario = ft.TextField(
        label="Usuario", 
        width=300, 
        border_color=ft.colors.LIGHT_BLUE, 
        filled=True, 
        fill_color=ft.colors.LIGHT_BLUE_50
    )
    contrasena = ft.TextField(
        label="Contraseña", 
        width=300, 
        password=True, 
        border_color=ft.colors.LIGHT_BLUE, 
        filled=True, 
        fill_color=ft.colors.LIGHT_BLUE_50
    )
    btn_iniciar_sesion = ft.ElevatedButton(
        text="Iniciar Sesión",
        on_click=iniciar_sesion,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE,
            shape=ft.RoundedRectangleBorder(radius=8),
            shadow=ft.BoxShadow(blur_radius=4, color=ft.colors.GREY)
        )
    )
    btn_registrar_usuario = ft.TextButton(
        text="Registrar Usuario",
        on_click=registrar_usuario,
        style=ft.ButtonStyle(
            color=ft.colors.BLUE,
            shape=ft.RoundedRectangleBorder(radius=8)
        )
    )
    btn_recuperar_contrasena = ft.TextButton(
        text="Recuperar Contraseña",
        on_click=recuperar_contrasena,
        style=ft.ButtonStyle(
            color=ft.colors.BLUE,
            shape=ft.RoundedRectangleBorder(radius=8)
        )
    )

    # Agregar los elementos a la página
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    usuario,
                    contrasena,
                    btn_iniciar_sesion,
                    btn_registrar_usuario,
                    btn_recuperar_contrasena,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            width=400,
            height=600,
            alignment=ft.alignment.center,
            border_radius=ft.BorderRadius.all(10),
            border=ft.Border.all(color=ft.colors.GREY_300),
            shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.GREY_300)
        )
    )

# Ejecutar la aplicación
ft.app(target=main)