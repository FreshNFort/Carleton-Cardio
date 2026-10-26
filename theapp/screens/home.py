
import flet as ft
import styles 


# CREATES A  BOX/CONTAINER OF TEXT. TITLE IS SMALLER, UNBOLDED, VALUE IS THE NUMBERED AMOUNT DISPLAY LARGER AND IN BOLD  
def stat_box(title: str,value:str) -> ft.Container:
    return ft.Container(
        **styles.BOX_STYLE,
        
        content=ft.Column(
            [
                ft.Text(title, **styles.BOX_TEXT_STYLE,),
                ft.Text(value, **styles.BOX_TEXT_STYLE, size=24, weight=ft.FontWeight.BOLD, )
            ],    

        ), 
          

    )
    
# HEADING TEXT STYLED FROM STYLES.PY
heading = ft.Text("Welcome!", **styles.HEADER_TEXT_STYLE,)

# HEADER ROW CONTAINING TEXT FROM HEADING
header = ft.Row(
    controls=[
        ft.Container(
            content=heading,
            expand = True, 
            alignment=ft.Alignment.TOP_CENTER,
        )
    ]
)

two_boxes_layout = ft.Row(
    controls=[
        stat_box("Distance:","3.2 km",), 
        stat_box("Time Spent:", "2.5 hrs"),
    ], 
)

# MAIN BODY
body = ft.SafeArea(
    content = ft.Row(
        controls= [
            # BOXES COLUMN
            ft.Column(
            [
                header,  
                ft.Text("Daily updates:",), 
                two_boxes_layout,   
                
            ],
            expand=True, #sets the column to 50% of screen



            ), 
            # RIGHT COLUMN
            ft.Column(
                ft.Container(
                    bgcolor="blue", #REDDD
                    content=ft.Text("Map here ?"),     
                    expand = True,     
                    
                ),
            expand=True, #sets the column to 50% of screen
            )

        ], 
        
    ), 
    
)

def home_view() -> ft.Control:
    return ft.Column(
        [
        body, 
    ],
    
    
    )
