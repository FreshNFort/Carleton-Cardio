import flet as ft

heading = ft.Text("Home", size=28, weight=ft.FontWeight.BOLD)
body = ft.Text("Testing ... body words here")

def home_view() -> ft.Control:
    return ft.Column(
        [
        
        ft.Container(
            content=heading,
            alignment=ft.Alignment.TOP_CENTER,
            # expand=True, 
        ),
        ft.Text("Testing ... body words here "), 
    ],
    spacing=16, 
    
    )
