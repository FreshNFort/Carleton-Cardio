
import flet as ft

def stat_card(title: str,value:str) -> ft.Card:
    return ft.Card(
        content=ft.Container(
            padding=16,
            content=ft.Column(
                [
                    ft.Text(title, size=14),
                    ft.Text(value,size=24, weight=ft.FontWeight.BOLD)
                ],
                spacing=4,
            ),
        )
    )

heading = ft.Text("Welcome!", size=28, text_align=ft.TextAlign.CENTER, weight = ft.FontWeight.BOLD)

header = ft.Row(
    controls=[
        ft.Container(
            content=heading,
            expand = True, 
            alignment=ft.Alignment.TOP_CENTER,
            # **BOX_STYLE,
        )
    ]
)

body = ft.SafeArea(
    content=ft.Column(
        [
            heading, 
            stat_card("Distance:","3.2 km"),
            stat_card("Buildings visited:", "4"),
        ],
        
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        scroll=ft.ScrollMode.AUTO,
        spacing=12,
        expand=True,
    ),
)

def home_view() -> ft.Control:
    return ft.Column(
        [
        body, 
    ],
    spacing=16, 
    
    )
