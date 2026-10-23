import flet as ft

def home_view() -> ft.Control:
    return ft.Column([
        ft.Text("Home", size=28, weight=ft.FontWeight.BOLD),
        ft.Button("Start tracking"),
    ], spacing=16)
