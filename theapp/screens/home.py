
import flet as ft
import styles 


# CREATES A  BOX/CONTAINER OF TEXT. TITLE IS SMALLER, UNBOLDED, VALUE IS THE NUMBERED AMOUNT DISPLAY LARGER AND IN BOLD  
def stat_box(title: str,value:str) -> ft.Container:
    return ft.Container(
        col={"xs": 6, "md": 3},
        **styles.BOX_STYLE,
        height = 100,

        gradient=styles.CARD_GRADIENT1,
        shadow=styles.CARD_SHADOW,
        content=ft.Column(
            [
                ft.Text(title, **styles.BOX_TEXT_STYLE1,),
                ft.Text(value, **styles.BOX_TEXT_STYLE1, size=24, weight=ft.FontWeight.BOLD, )
            ],    
        ), 
    )
          
    
# HEADER ROW CONTAINING HEADING TEXT
header = ft.Row(
    controls=[
        ft.Container(
            padding = ft.Padding.only(top=25),
            content=ft.Text("Welcome!", style=ft.TextStyle(size=32, shadow = styles.HEADING_SHADOW, font_family = "Segoe UI", **styles.HEADING1_TEXT_STYLE),
                ),
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

leaderboard_box = ft.Container(
        col={"xs": 12, "md": 12},
        **styles.BOX_STYLE,
        height = 130,
        
        gradient=styles.CARD_GRADIENT2,
        shadow=styles.CARD_SHADOW,
        content=ft.Column(
            [
                ft.Text("Leaderboard Position:", **styles.BOX_TEXT_STYLE2, weight=ft.FontWeight.W_500,),
                ft.Text("3rd", **styles.BOX_TEXT_STYLE2, size=30, weight=ft.FontWeight.BOLD, ),
                ft.Text("You're x points behind y!", **styles.BOX_TEXT_STYLE2,),
            ],    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ), 
    )


record_button = ft.Button(
    content = "Record"
)


def home_view() -> ft.Control:

    return ft.Column(
        scroll=ft.ScrollMode.HIDDEN,
        # alignment=ft.MainAxisAlignment.START,
        alignment = ft.Alignment(0, -1),
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH, 
        expand=True,
        
        controls = 
        [
        ft.SafeArea(
            content=ft.ResponsiveRow(
            # spacing=15,
            # run_spacing=15,
            width = 100,
            controls=[
                header,
                # HEADER
                ft.Row(
                    controls=[
                        ft.Container(
                            content= ft.Text("Explore your dashboard", size = 16,  **styles.HEADING2_TEXT_STYLE, ),
                        ),
                        
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),  
                # BOXES COLUMN 
                ft.Container(
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        controls=[
                            ft.Text("Daily updates:", **styles.HOME_PARAGRAPH_TEXT),
                            two_boxes_layout,
                            leaderboard_box, 
                        ]
                    ),
                ),
                # RIGHT COLUMN 
                ft.Container(
                    content= ft.Column(
                        controls=[ 
                        ft.Text("Start a new session?", size = 16,  **styles.HEADING2_TEXT_STYLE, ),
                        ]
                    )
                    
                    
                ),
            ],
        ),
    ), 
],
        
)
