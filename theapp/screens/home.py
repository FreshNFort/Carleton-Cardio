import flet as ft
import styles 

#NEWW
#from Profiles.activities import get_user_totals, get_user_rank  # replace 'database' with your teammate's file name
from Profiles.activities import get_user_totals
#from Profiles.user_profiles import get_user_profile
from Profiles.leaderboard import get_leaderboard

USER_ID = "noah fortin"  # test user, same one profile_view uses

def load_distance() -> str:
    """Fetches the user's total distance from Firebase, formatted for the stat box."""
    try:
        totals = get_user_totals(USER_ID)
        return f"{totals['distance_km']} km"
    except Exception as e:
        print("Could not load distance:", e)
        return "--"

#NEWW
def ordinal(n: int) -> str:
    """1 -> '1st', 2 -> '2nd', 3 -> '3rd', 11 -> '11th', 21 -> '21st'."""
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def load_rank() -> str:
    """Finds the user on the leaderboard and returns their position, e.g. '3rd'."""
    try:
        for entry in get_leaderboard():
            if entry["uid"] == USER_ID:
                return ordinal(entry["rank"])
        return "--"
    except Exception as e:
        print("Could not load rank:", e)
        return "--"


#def load_rank() -> str:
   # """Fetches the user's leaderboard position and formats it for the home screen."""
   # try:
    #    rank = get_user_rank(USER_ID)
    #    return ordinal(rank) if rank else "--"
   # except Exception as e:
       # print("Could not load rank:", e)
        #return "--"


# CREATES A  BOX/CONTAINER OF TEXT. TITLE IS SMALLER, UNBOLDED, VALUE IS THE NUMBERED AMOUNT DISPLAY LARGER AND IN BOLD  
def stat_box(title: str, value: str, col=None) -> ft.Container:
    return ft.Container(
        col= col or{"xs": 6, "md": 3},
        **styles.BOX_STYLE,
        height = 105,

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

"""
two_boxes_layout = ft.ResponsiveRow(
    spacing=10,  
    run_spacing=10,
    controls=[
        stat_box("Distance:", "3.2 km"),
        stat_box("Time Spent:", "2.5 hrs"),
    ],
)
"""


record_button = ft.Button(
    style = styles.RECORD_BUTTON,
    content=ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Text("Record", size=18),
            ft.Icon(ft.Icons.ADJUST_OUTLINED, color="#FFE8EA",),
        ],
    )
)


def home_view(on_leaderboard_click=None) -> ft.Control:

    distance_text = load_distance()
    rank_text = load_rank()
    
    leaderboard_button = ft.Button(
        style = styles.LEADERBOARD_BUTTON,
        on_click=on_leaderboard_click,
            content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("View Leaderboard", size=14),
                ft.Icon(ft.Icons.LEADERBOARD_ROUNDED, color="#FFE8EA",),
            ],
        )

    )
    leaderboard_box = ft.Container(
            col={"xs": 12, "md": 12},
            **styles.BOX_STYLE,
            height = 200,
            gradient=styles.CARD_GRADIENT2,
            shadow=styles.CARD_SHADOW,
            content=ft.Column(
                [
                    ft.Text("Leaderboard Position:", **styles.BOX_TEXT_STYLE2, size = 20, weight=ft.FontWeight.W_600,),
                    ft.Text(rank_text, **styles.BOX_TEXT_STYLE2, size=32, weight=ft.FontWeight.BOLD),
                    #ft.Text("3rd", **styles.BOX_TEXT_STYLE2, size=32, weight=ft.FontWeight.BOLD, ),
                    leaderboard_button,  
                ],    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ), 
        )

    distance_box = stat_box("Distance:", distance_text, col={"xs": 12, "md": 12})
    
    #two_boxes_layout = ft.ResponsiveRow(
        #spacing=10,
        #run_spacing=10,
        #controls=[
            #stat_box("Distance:", distance_text),
            #stat_box("Time Spent:", time_text),
        #],
    #)


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
                            content= ft.Text("Explore your dashboard", size = 16,  **styles.HOME_PARAGRAPH_TEXT, ),
                        ),
                        
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),  
                # BOXES COLUMN 
                ft.Container(
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        controls=[
                            # ft.Text("Daily updates:", **styles.HOME_PARAGRAPH_TEXT),
                            #two_boxes_layout,
                            distance_box,
                            leaderboard_box, 
                        ]
                    ),
                ),
                # RIGHT COLUMN 
                ft.Container(
                    content= ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        controls=[ 
                        ft.Text("Start a new session?", size = 16,  **styles.HEADING2_TEXT_STYLE, ),
                        record_button, 
                        ]
                    )
                    
                    
                ),
            ],
        ),
    ), 
],
        
)
