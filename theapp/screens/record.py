import flet as ft

def record_view() -> ft.Control:
    return ft.Column([
        ft.Text("Record", size=28, weight=ft.FontWeight.BOLD),
    ], spacing=16)
