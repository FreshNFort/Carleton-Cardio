from fastapi.datastructures import Default
import flet as ft

# styling for box elements 
BOX_STYLE = {
#    "bgcolor": "#7C2932",
    "border_radius": 12,           
    "padding": 15,                 
    "height": 100, 
}

BOX_TEXT_STYLE = {
    "color": "#FFE8EA",   
    "text_align": ft.TextAlign.CENTER, 

}


# HEADER_TEXT_STYLE = ft.TextStyle(
#     color="#FFFBFB",
#     size=28, 
#     text_align=ft.TextAlign.CENTER, 
#     weight = ft.FontWeight.BOLD,
# )

HEADER_TEXT_STYLE = {
    "weight": ft.FontWeight.BOLD,
    "color": "#551414",
}

BODY_STYLE = {
    "bgcolor":  "#FFE8EA",
}

CARD_GRADIENT = ft.LinearGradient(
    begin=ft.Alignment.TOP_LEFT,
    end=ft.Alignment.BOTTOM_RIGHT,
    colors=["#7C2932", "#91434C"],
)

CARD_SHADOW = ft.BoxShadow(
    spread_radius=1,
    blur_radius=10,
    color=ft.Colors.with_opacity(
        0.2, ft.Colors.BLACK
    ),  # Semi-transparent shadow
    offset=ft.Offset(0, 4),  # Shifts shadow slightly downward
)

HOME_PARAGRAPH_TEXT = {
    "color":"#551414",
    "italic": True,
}



# APP_THEME = ft.Theme(
#     navigation_bar_theme=ft.NavigationBarTheme(
#         bgcolor="#1c4ab4", 
#         indicator_color="#312e81",  
#         elevation=8,
#         label_text_style=ft.TextStyle(
#             color=ft.Colors.WHITE_70, size=12, weight=ft.FontWeight.W_500
#         ),
#     ),
# )




NAV_BG_COLOR = "#5C2424"

NAV_INDICATOR_COLOR = "#963838"

