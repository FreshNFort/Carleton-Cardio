import flet as ft

# styling for box elements 
BOX_STYLE = {
   "bgcolor": "#FFE0E3",
    "border_radius": 12,           
    "padding": 15,                 
    # "width": 150,                 
    "height": 100, 
    "expand": True, #sets the boxes to fill container
}

BOX_TEXT_STYLE = {
    "color": "#64242A",   
    "text_align": ft.TextAlign.CENTER, 

}


# HEADER_TEXT_STYLE = ft.TextStyle(
#     color="#FFFBFB",
#     size=28, 
#     text_align=ft.TextAlign.CENTER, 
#     weight = ft.FontWeight.BOLD,
# )

HEADER_TEXT_STYLE = {
    "size": 28,
    "weight": ft.FontWeight.BOLD,
    "color": "#551414",
    "text_align": ft.TextAlign.CENTER, 
    "expand": True                   
}

BODY_STYLE = {
    "bgcolor":  "#FFFFFF",
}