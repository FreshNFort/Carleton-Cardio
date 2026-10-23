import flet as ft

def leaderboard_view() -> ft.Control:
    return ft.Column([
        ft.Text("Leaderboard", size=28, weight=ft.FontWeight.BOLD),

    ], spacing=16)
