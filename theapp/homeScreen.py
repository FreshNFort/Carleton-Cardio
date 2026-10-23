# import flet as ft

# def main(page: ft.Page):
#     page.theme = ft.Theme(color_scheme_seed="teal")
#     page.title = "NavigationBar Example"

#     page.navigation_bar = ft.NavigationBar(
#         destinations=[
#             ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Maps"),
#             ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE_OUTLINED, label="Profile"),
#             ft.NavigationBarDestination(icon=ft.Icons.QUERY_STATS, label="Stats"),
#             ft.NavigationBarDestination(icon=ft.Icons.ACCESS_TIME, label="Record"),


#         ]
#     )

#     page.bgcolor = "#880111"  # hex string; a named constant like ft.Colors.BLUE_GREY_900 also works
#     page.add(ft.Text("Welcome!", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE))


#     page.add(
#         ft.SafeArea(
#             content=ft.Text("Body!"),


#         )
#     )

# if __name__ == "__main__":
#     ft.run(main)

import flet as ft

def home_view() -> ft.Control:
    return ft.Column([
        ft.Text("Home", size=28, weight=ft.FontWeight.BOLD),
        ft.Button("Start tracking"),
    ], spacing=16)
