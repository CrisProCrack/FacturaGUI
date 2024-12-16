import flet as ft
from flet import *
from db_config import DatabaseConnection
import hashlib
import billing
import billing_visualitation
import customers
import products

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_login(username, password):
    conn = DatabaseConnection.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            hashed_password = hash_password(password)
            query = "SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s"
            cursor.execute(query, (username, hashed_password))
            result = cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"Error during login: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def register_user(username, password, confirm_password, email, phone):
    if not all([username, password, confirm_password, email, phone]):
        return "Por favor complete todos los campos"

    if password != confirm_password:
        return "Las contraseñas no coinciden"

    conn = DatabaseConnection.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            hashed_password = hash_password(password)
            
            # Verificar si el usuario ya existe
            cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (username,))
            if cursor.fetchone():
                return "El usuario ya existe"

            # Insertar nuevo usuario
            query = """
            INSERT INTO usuarios (usuario, contrasena, correo, telefono) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (username, hashed_password, email, phone))
            conn.commit()
            return "Registro exitoso"
        except Exception as e:
            print(f"Error during registration: {e}")
            return "Error al registrar usuario"
        finally:
            cursor.close()
            conn.close()
    return "Error de conexión a la base de datos"

def validate_user_email(username, email):
    conn = DatabaseConnection.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM usuarios WHERE usuario = %s AND correo = %s"
            cursor.execute(query, (username, email))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error validating user email: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def update_password(username, new_password):
    conn = DatabaseConnection.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            hashed_password = hash_password(new_password)
            query = "UPDATE usuarios SET contrasena = %s WHERE usuario = %s"
            cursor.execute(query, (hashed_password, username))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def show_dialog(page: Page, title: str, message: str):
    def close_dialog(e):
        dlg.open = False
        page.update()

    dlg = AlertDialog(
        modal=True,
        title=Text(title),
        content=Text(message),
        actions=[
            TextButton("OK", on_click=close_dialog),
        ],
        actions_alignment=MainAxisAlignment.END,
    )
    
    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def create_login_view(page: Page, on_login_success):
    def on_register_success():
        page.controls.clear()
        page.add(create_login_view(page, on_login_success))
        page.update()

    def handle_login(e):
        username = usuario.value
        password = contraseña.value
        
        if not username or not password:
            show_dialog(page, "Error", "Por favor complete todos los campos")
            return
        
        if validate_login(username, password):
            show_dialog(page, "Éxito", "Inicio de sesión exitoso")
            on_login_success()
        else:
            show_dialog(page, "Error", "Usuario o contraseña incorrectos")

    def go_to_register(e):
        page.controls.clear()
        page.add(create_register_view(page, on_register_success, on_login_success))
        page.update()

    def go_to_recovery(e):
        page.controls.clear()
        page.add(create_recovery_view(page, on_recovery_success))
        page.update()

    def on_recovery_success():
        page.controls.clear()
        page.add(create_login_view(page, on_login_success))
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
    recuperar_password = TextButton(
        text="¿Olvidaste tu contraseña?",
        style=ButtonStyle(color={"": Colors.PINK_50}),
        on_click=go_to_recovery
    )
    iniciar_sesion = FilledButton(
        text="Iniciar Sesión",
        width=300,  # Cambiado para que coincida con el ancho de los otros elementos
        height=40,
        on_click=handle_login
    )
    
    return Container(
        content=Card(
            content=Container(
                content=Column(
                    [headline, usuario, contraseña, registrate, recuperar_password, iniciar_sesion],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                padding=20,
                width=400,  # Cambiado para ser consistente
                height=None,  # Altura automática
                alignment=alignment.center,
            ),
            elevation=2
        ),
        alignment=alignment.center,
        expand=True
    )

def create_register_view(page: Page, on_register_success, on_login_success):
    def validate_email(email):
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_phone(phone):
        return phone.isdigit() and len(phone) >= 10

    def on_username_change(e):
        if len(usuario.value) < 4:
            usuario.helper_text = "El usuario debe tener al menos 4 caracteres"
            usuario.border_color = Colors.ERROR
        else:
            usuario.helper_text = "Usuario válido"
            usuario.border_color = Colors.GREEN
        page.update()

    def on_password_change(e):
        if len(contraseña.value) < 8:
            contraseña.helper_text = "La contraseña debe tener al menos 8 caracteres"
            contraseña.border_color = Colors.ERROR
        else:
            contraseña.helper_text = "Contraseña válida"
            contraseña.border_color = Colors.GREEN
        validate_passwords()
        page.update()

    def on_confirm_password_change(e):
        validate_passwords()
        page.update()

    def validate_passwords():
        if contraseña.value != contraseña_validate.value:
            contraseña_validate.helper_text = "Las contraseñas no coinciden"
            contraseña_validate.border_color = Colors.ERROR
        else:
            contraseña_validate.helper_text = "Las contraseñas coinciden"
            contraseña_validate.border_color = Colors.GREEN

    def on_email_change(e):
        if not validate_email(correo.value):
            correo.helper_text = "Formato de correo inválido"
            correo.border_color = Colors.ERROR
        else:
            correo.helper_text = "Correo válido"
            correo.border_color = Colors.GREEN
        page.update()

    def on_phone_change(e):
        if not validate_phone(telefono.value):
            telefono.helper_text = "Solo números (al menos 10 dígitos)"
            telefono.border_color = Colors.ERROR
        else:
            telefono.helper_text = "Teléfono válido"
            telefono.border_color = Colors.GREEN
        page.update()

    def handle_register(e):
        if (len(usuario.value) >= 4 and
            len(contraseña.value) >= 8 and
            contraseña.value == contraseña_validate.value and
            validate_email(correo.value) and
            validate_phone(telefono.value)):
            result = register_user(usuario.value, contraseña.value, 
                                 contraseña_validate.value, correo.value, 
                                 telefono.value)
            if result == "Registro exitoso":
                show_dialog(page, "Éxito", "Usuario registrado exitosamente")
                on_register_success()
            else:
                show_dialog(page, "Error", result)
        page.update()
    
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
        prefix_icon=Icons.PERSON,
        helper_text="Mínimo 4 caracteres",
        on_change=on_username_change,
        border_color=Colors.PINK,
        focused_border_color=Colors.PINK,
        helper_style=TextStyle(size=12)
    )
    
    contraseña = TextField(
        label="Contraseña",
        width=300,
        password=True,
        can_reveal_password=True,
        prefix_icon=Icons.LOCK,
        helper_text="Mínimo 8 caracteres",
        on_change=on_password_change,
        border_color=Colors.PINK,
        focused_border_color=Colors.PINK,
        helper_style=TextStyle(size=12)
    )
    
    contraseña_validate = TextField(
        label="Confirmar Contraseña",
        width=300,
        password=True,
        can_reveal_password=True,
        prefix_icon=Icons.LOCK,
        helper_text="Repita la contraseña",
        on_change=on_confirm_password_change,
        border_color=Colors.PINK,
        focused_border_color=Colors.PINK,
        helper_style=TextStyle(size=12)
    )
    
    correo = TextField(
        label="Correo",
        width=300,
        prefix_icon=Icons.EMAIL,
        helper_text="ejemplo@dominio.com",
        on_change=on_email_change,
        border_color=Colors.PINK,
        focused_border_color=Colors.PINK,
        helper_style=TextStyle(size=12)
    )
    
    telefono = TextField(
        label="Teléfono",
        width=300,
        prefix_icon=Icons.PHONE,
        helper_text="Solo números (al menos 10 dígitos)",
        on_change=on_phone_change,
        border_color=Colors.PINK,
        focused_border_color=Colors.PINK,
        helper_style=TextStyle(size=12)
    )

    label_iniciar_sesion = TextButton(
        text="¿Ya tienes una cuenta? Inicia sesión",
        style=ButtonStyle(color={"": Colors.PINK_50}),
        on_click=go_to_login
    )

    registrar = FilledButton(
        text="Registrarse",
        width=300,
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
                padding=30,
                width=400,
                # Height will adjust automatically based on content
                alignment=alignment.center,
            ),
            elevation=2
        ),
        alignment=alignment.center,
        expand=True
    )

def create_recovery_view(page: Page, on_recovery_success):
    def handle_recovery(e):
        if not username.value or not email.value or not new_password.value or not confirm_password.value:
            show_dialog(page, "Error", "Por favor complete todos los campos")
            return
        
        if new_password.value != confirm_password.value:
            show_dialog(page, "Error", "Las contraseñas no coinciden")
            return

        if validate_user_email(username.value, email.value):
            if update_password(username.value, new_password.value):
                show_dialog(page, "Éxito", "Contraseña actualizada correctamente")
                page.controls.clear()  # Limpiar antes de cambiar vista
                on_recovery_success()
            else:
                show_dialog(page, "Error", "Error al actualizar la contraseña")
        else:
            show_dialog(page, "Error", "Usuario o correo no coinciden")

    def go_back(e):
        page.controls.clear()  # Limpiar antes de cambiar vista
        on_recovery_success()

    headline = Text("Recuperar Contraseña", theme_style=TextThemeStyle.HEADLINE_LARGE)
    
    username = TextField(
        label="Usuario",
        width=300,
        prefix_icon=Icons.PERSON,
    )
    
    email = TextField(
        label="Correo electrónico",
        width=300,
        prefix_icon=Icons.EMAIL,
    )
    
    new_password = TextField(
        label="Nueva contraseña",
        width=300,
        password=True,
        can_reveal_password=True,
        prefix_icon=Icons.LOCK,
    )
    
    confirm_password = TextField(
        label="Confirmar contraseña",
        width=300,
        password=True,
        can_reveal_password=True,
        prefix_icon=Icons.LOCK,
    )

    recuperar = FilledButton(
        text="Cambiar Contraseña",
        width=300,
        on_click=handle_recovery
    )

    volver = TextButton(
        text="Volver al inicio de sesión",
        style=ButtonStyle(color={"": Colors.PINK_50}),
        on_click=go_back
    )

    return Container(
        content=Card(
            content=Container(
                content=Column(
                    [headline, username, email, new_password, confirm_password, recuperar, volver],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                padding=30,
                width=400,
                alignment=alignment.center,
            ),
            elevation=2
        ),
        alignment=alignment.center,
        expand=True
    )

def main(page: ft.Page):
    page.clean()  # Limpiar la página al iniciar

    def show_main_app():
        page.controls.clear()
        
        # Create instances of each view
        products_view = products.create_products_view(page)
        customers_view = customers.create_customers_view(page)
        billing_view = billing.create_billing_view(page)
        billing_visualization_view = billing_visualitation.create_billing_visualization_view(page)

        views = [products_view, customers_view, billing_view, billing_visualization_view]
        current_view = views[0]

        def handle_logout(e):
            page.controls.clear()
            page.add(create_login_view(page, show_main_app))
            page.update()

        def change_nav(e):
            nonlocal current_view
            index = e.control.selected_index
            if index == 4:  # Si se selecciona cerrar sesión
                page.controls.clear()
                page.add(create_login_view(page, show_main_app))
                return
            
            page.controls.pop()
            current_view = views[index]
            
            # Actualizar datos si se cambia a la vista de facturación
            if index == 2:  # índice 2 corresponde a la vista de facturación
                # Forzar actualización de datos
                if hasattr(current_view, 'refresh_data'):
                    current_view.refresh_data()
            
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
                    label="Reimpresión \n de facturas",
                ),
                NavigationRailDestination(
                    icon=Icons.LOGOUT,
                    selected_icon=Icons.LOGOUT,
                    label="Cerrar Sesión",
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