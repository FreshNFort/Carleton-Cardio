import flet as ft

def profile_view() -> ft.Control:
    return ft.Column([
        ft.Text("Profile", size=28, weight=ft.FontWeight.BOLD),
    ], spacing=16)
