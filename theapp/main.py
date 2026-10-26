import flet as ft
import styles

from screens.home import home_view
from screens.map import map_view
from screens.profile import profile_view
from screens.stats import stats_view
from screens.record import record_view
from screens.leaderboard import leaderboard_view


SCREENS = [home_view, map_view, stats_view, leaderboard_view, profile_view, ]  # same order as the navbar destinations

def main(page: ft.Page):


    page.title = "Mobile Preview Simulator"

    # PHONE SIMULATOR COMMANDS
    page.window.width = 350
    page.window.height = 744

    page.window.min_width = 360
    page.window.max_width = 430
    page.window.min_height = 640
    page.window.max_height = 932
   


    page.title = "Carleton Cardio"
    page.on_error = lambda e: print(f"Flet Error: {e.data}")
    page.theme = ft.Theme(color_scheme_seed="red")
    page.bgcolor = "#F5C3C5"
    

    body = ft.Container(content=SCREENS[0](), padding=20)

    def on_nav_change(e):
        body.content = SCREENS[e.control.selected_index]()
        page.update()

    page.navigation_bar = ft.NavigationBar(
        label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Home"),
            # ft.NavigationBarDestination(icon=ft.Icons.ACCESS_TIME, label="Record"),
            ft.NavigationBarDestination(icon=ft.Icons.MAP_OUTLINED, label="Maps"),
            ft.NavigationBarDestination(icon=ft.Icons.QUERY_STATS, label="Stats"),
            ft.NavigationBarDestination(icon=ft.Icons.LEADERBOARD_OUTLINED, label="Leader\nboard"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE_OUTLINED, label="Profile"),

        ],
        on_change=on_nav_change,
        bgcolor=styles.NAV_BG_COLOR,
        indicator_color=styles.NAV_INDICATOR_COLOR,
        

    )

    page.add(ft.SafeArea(body))
    page.update()




ft.run(main)

