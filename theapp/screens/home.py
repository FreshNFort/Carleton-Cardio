
import flet as ft
import styles 


# CREATES A  BOX/CONTAINER OF TEXT. TITLE IS SMALLER, UNBOLDED, VALUE IS THE NUMBERED AMOUNT DISPLAY LARGER AND IN BOLD  
def stat_box(title: str,value:str) -> ft.Container:
    return ft.Container(
        # col={"xs": 12, "md": 6},
        **styles.BOX_STYLE,
        gradient=styles.CARD_GRADIENT,
        shadow=styles.CARD_SHADOW,
        content=ft.Column(
            [
                ft.Text(title, **styles.BOX_TEXT_STYLE,),
                ft.Text(value, **styles.BOX_TEXT_STYLE, size=24, weight=ft.FontWeight.BOLD, )
            ],    
        ), 
    )
          
    

# HEADER ROW CONTAINING HEADING TEXT
header = ft.Row(
    controls=[
        ft.Container(
            content=ft.Text("Welcome!", size=28,  font_family = "Segoe UI",**styles.HEADER_TEXT_STYLE),
            
        ),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
)

two_boxes_layout = ft.ResponsiveRow(
    spacing=10,  
    run_spacing=10,
    controls=[
        stat_box("Distance:", "3.2 km"),
        stat_box("Time Spent:", "2.5 hrs"),
    ],
)



def home_view() -> ft.Control:

    
    return ft.Column(
        [
        ft.SafeArea(
        content=ft.ResponsiveRow(
            spacing=15,
            run_spacing=15,
            controls=[
                header,
                # HEADER
                ft.Row(
                    controls=[
                        ft.Container(
                            content= ft.Text("Explore your dashboard", size = 16,  **styles.HEADER_TEXT_STYLE, ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),  

                # BOXES COLUMN 
                ft.Container(
                    col={"xs": 12, "md": 6},  # full width on mobile, half on desktop
                    content=ft.Column(
                        controls=[
                            ft.Text("Daily updates:", **styles.HOME_PARAGRAPH_TEXT),
                            two_boxes_layout,
                        ]
                    ),
                ),
                # RIGHT COLUMN 
                ft.Container(
                    col={"xs": 12, "md": 6},  # full width on mobile, half on desktop
                    content=ft.Text("Map here ?"),
                ),
            ],
        ),
    ), 
],
    
    
)
