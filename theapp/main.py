import flet as ft
import styles

from screens.home import home_view
from screens.map import map_view
from screens.leaderboardview import leaderboard_view
from Profiles.user_profiles import get_user_profile

HOME, MAP, LEADERBOARD = range(3)  # same order as the navbar destinations
PROFILE_USER_ID = "noah fortin"


def profile_view() -> ft.Control:
    try:
        profile = get_user_profile(PROFILE_USER_ID) or {}
    except Exception as error:
        print(f"Could not load profile: {error}")
        profile = {}
    username = profile.get("username", "User")
    total_distance = profile.get("total_distance_km", 0.0)

    header = ft.Row(
        controls=[
            ft.Container(
                padding=ft.Padding.only(top=25),
                content=ft.Text(
                    f"Welcome, {username}!",
                    style=ft.TextStyle(
                        size=28,
                        shadow=styles.HEADING_SHADOW,
                        font_family="Segoe UI",
                        **styles.HEADING1_TEXT_STYLE,
                    ),
                ),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=16,
        controls=[
            header,
            ft.Text(f"Total Distance: {total_distance} km", size=20, weight=ft.FontWeight.BOLD),
        ],
    )


def main(page: ft.Page):
    page.title = "Carleton Cardio"
    page.padding = 0
    page.theme = ft.Theme(color_scheme_seed="red")
    page.bgcolor = "#F5C3C5"
    page.on_error = lambda e: print(f"Flet Error: {e.data}")

    # Phone simulator window (desktop only)
    page.window.width = 390
    page.window.height = 744
    page.window.min_width = 360
    page.window.max_width = 430
    page.window.min_height = 640
    page.window.max_height = 932

    body = ft.Container(padding=ft.Padding.symmetric(horizontal=20), expand=True)
    map_screen = None  # created once so an active recording survives tab switches

    def get_map(start_immediately: bool = False):
        nonlocal map_screen
        if map_screen is None:
            map_screen = map_view(page, include_home=False, start_immediately=start_immediately)
        return map_screen

    def show(index: int, start_recording: bool = False):
        if index == HOME:
            body.content = home_view(on_record=go_record)
        elif index == MAP:
            body.content = get_map(start_immediately=start_recording)
        elif index == LEADERBOARD:
            body.content = leaderboard_view()
        else:
            body.content = profile_view()
        page.update()

    def go_record(e=None):
        page.navigation_bar.selected_index = MAP
        show(MAP, start_recording=True)

    def on_nav_change(e):
        show(e.control.selected_index)

    page.navigation_bar = ft.NavigationBar(
        label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.MAP_OUTLINED, label="Maps"),
            ft.NavigationBarDestination(icon=ft.Icons.LEADERBOARD_OUTLINED, label="Leader\nboard"),
            # ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE_OUTLINED, label="Profile"),
        ],
        on_change=on_nav_change,
        bgcolor=styles.NAV_BG_COLOR,
        indicator_color=styles.NAV_INDICATOR_COLOR,
    )

    body.content = home_view(on_record=go_record)
    page.add(ft.SafeArea(body, expand=True))


ft.run(main)