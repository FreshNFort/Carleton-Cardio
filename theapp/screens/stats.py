import flet as ft

def stats_view() -> ft.Control:
    return ft.Column([
        ft.Text("Stats", size=28, weight=ft.FontWeight.BOLD),
        ft.Button("Start tracking"),
    ], spacing=16)
