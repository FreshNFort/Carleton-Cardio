from fastapi.datastructures import Default
import flet as ft

# styling for box elements 
BOX_STYLE = {
#    "bgcolor": "#7C2932",
    "border_radius": 12,           
    "padding": 15,                 
    # "height": 100, 
}

BOX_TEXT_STYLE1 = {
    "color": "#FFE8EA",   
    "text_align": ft.TextAlign.CENTER, 

}


BOX_TEXT_STYLE2 = {
    "color": "#5C111A",   
    "text_align": ft.TextAlign.CENTER, 

}

HEADING1_TEXT_STYLE = {
    "weight": ft.FontWeight.W_800,
    "color": "#501D23",
}

HEADING2_TEXT_STYLE = {
    "weight": ft.FontWeight.W_600,
    "color": "#551414",
}

BODY_STYLE = {
    "bgcolor":  "#FFE8EA",
}

HEADING_SHADOW = ft.BoxShadow(
    blur_radius=3.0,  
    color=ft.Colors.with_opacity(
        0.2, ft.Colors.BLACK
    ),  
    offset=ft.Offset(1, 2),  # X and Y shift (horizontal, vertical)
)

CARD_GRADIENT1 = ft.LinearGradient(
    begin=ft.Alignment.TOP_LEFT,
    end=ft.Alignment.BOTTOM_RIGHT,
    colors=["#7C2932", "#91434C"],
)

CARD_GRADIENT2 = ft.LinearGradient(
    begin=ft.Alignment.TOP_LEFT,
    end=ft.Alignment.BOTTOM_RIGHT,
    colors=["#FFF4F5", "#F8DDDE"],
)


CARD_SHADOW = ft.BoxShadow(
    spread_radius=1,
    blur_radius=10,
    color=ft.Colors.with_opacity(
        0.2, ft.Colors.BLACK
    ),  
    offset=ft.Offset(0, 4),  # Shifts shadow slightly downward
)

HOME_PARAGRAPH_TEXT = {
    "color":"#551414",
    "italic": True,
}


NAV_BG_COLOR = "#5C2424"

NAV_INDICATOR_COLOR = "#7E3737"

