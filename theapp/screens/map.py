import flet as ft

def map_view() -> ft.Control:
    return ft.Column([
        ft.Text("Map", size=28, weight=ft.FontWeight.BOLD),
        ft.Button("Start tracking"),
    ], spacing=16)
