import flet as ft

from screens.home import home_view
from screens.map import map_view
from screens.profile import profile_view
from screens.stats import stats_view
from screens.record import record_view
from screens.leaderboard import leaderboard_view


SCREENS = [home_view, record_view, map_view, stats_view, leaderboard_view, profile_view, ]  # same order as the navbar destinations

def main(page: ft.Page):
    page.title = "Carleton Cardio"
    page.theme = ft.Theme(color_scheme_seed="red")
    

    body = ft.Container(content=SCREENS[0](), padding=20, expand=True)

    def on_nav_change(e):
        body.content = SCREENS[e.control.selected_index]()
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.ACCESS_TIME, label="Record"),
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Maps"),
            ft.NavigationBarDestination(icon=ft.Icons.QUERY_STATS, label="Stats"),
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Leaderboard"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE_OUTLINED, label="Profile"),

        ],
        on_change=on_nav_change,
    )

    page.add(ft.SafeArea(body, expand=True))




ft.run(main)

