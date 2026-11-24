import flet as ft
from Profiles.leaderboard import get_leaderboard

def main(page: ft.Page):
    page.title = "Leaderboard"
    page.window.width = 350
    page.window.height = 744
    page.padding = 0
    page.bgcolor = "#5C2424"
    page.theme_mode = ft.ThemeMode.LIGHT

    #Data
    leaderboard = get_leaderboard()

    weekly_data = []
    for user in leaderboard:
        weekly_data.append({"rank": user["rank"], "name": user["username"], "points": f"{user["total_distance_km"]} km"})
        

    podium_container = ft.Row(
        alignment = ft.MainAxisAlignment.CENTER,
        vertical_alignment = ft.CrossAxisAlignment.END,
        spacing = 8,
    )
    list_view = ft.ListView(expand = True, spacing = 10, padding = 15)

    def build_podium_step(user: dict, rank: int, bar_height: int, bar_color: str, is_first: bool = False):

        return ft.Column(
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 6,
            controls = [
                ft.Text(
                    user["name"].split()[0],
                    color = ft.Colors.WHITE,
                    weight = ft.FontWeight.BOLD,
                    size = 14,
                    max_lines = 1,
                    overflow = ft.TextOverflow.ELLIPSIS,
                ),
                ft.Container(
                    content = ft.Text(user["points"], color = ft.Colors.WHITE, size = 11, weight = ft.FontWeight.W_600),
                    bgcolor = "#8879F0",
                    padding = 10,
                    border_radius = 12,
                ),
                ft.Container(
                    width = 95,
                    height = bar_height,
                    bgcolor = bar_color,
                    border_radius = 14,
                    padding = 10, 
                    content = ft.Text(
                        str(rank),
                        size = 38 if is_first else 30,
                        weight = ft.FontWeight.BOLD,
                        color = ft.Colors.WHITE,
                        text_align = ft.TextAlign.CENTER,
                    ),
                ),
            ],
        )

    def build_rank_row(user: dict):
        return ft.Container(
            bgcolor = ft.Colors.WHITE,
            border_radius = 16,
            padding = 12,
            shadow = ft.BoxShadow(
                spread_radius = 0,
                blur_radius = 8,
                color = ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                offset = ft.Offset(0, 3),
            ),
            content = ft.Row(
                alignment = ft.MainAxisAlignment.START,
                spacing = 12,
                controls = [
                    ft.Container(
                        content = ft.Text(
                            str(user["rank"]),
                            size = 13,
                            weight = ft.FontWeight.BOLD,
                            color = "#7E7C8E",
                        ),
                        padding = 5,
                        width = 26,
                        height = 26,
                        border_radius = 13,
                    ),
                    ft.Column(
                        spacing = 2,
                        controls = [
                            ft.Text(user["name"], weight = ft.FontWeight.BOLD, size = 14, color = "#1D1B20"),
                            ft.Text(user["points"], size = 12, color = "#858494"),
                        ],
                    ),
                ],
            ),
        )

    # Populate Podium 
    podium_container.controls = [
        build_podium_step(weekly_data[1], rank = 2, bar_height = 105, bar_color = "#FDB773"),
        build_podium_step(weekly_data[0], rank = 1, bar_height = 135, bar_color = "#FDB773", is_first = True),
        build_podium_step(weekly_data[2], rank = 3, bar_height = 85, bar_color = "#FDB773"),
    ]
    list_view.controls = [build_rank_row(u) for u in weekly_data[3:]]

    # Top Header Bar
    header = ft.Container(
        padding = 15,
        content = ft.Row(
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            controls = [
                ft.IconButton(icon = ft.Icons.ARROW_BACK_IOS_NEW, icon_color = ft.Colors.WHITE, icon_size = 18),
                ft.Text("Leaderboard", size = 20, weight = ft.FontWeight.BOLD, color = ft.Colors.WHITE),
                ft.IconButton(icon = ft.Icons.MORE_VERT, icon_color = ft.Colors.WHITE, icon_size = 20),
            ],
        ),
    )

    # Title label
    title_banner = ft.Container(
        content = ft.Row(
            alignment = ft.MainAxisAlignment.CENTER,
            controls = [ft.Text("Weekly Ranking", color = ft.Colors.WHITE, weight = ft.FontWeight.BOLD, size = 14)]
        ),
        bgcolor = "#5849C9",
        padding = 10,
        border_radius = 16,
    )


    # Bottom White Sheet
    bottom_sheet = ft.Container(
        expand = True,
        bgcolor = "#F8F7FC",
        border_radius = 28,
        padding = 15,
        content = list_view,
    )

    # Main Layout
    page.add(
        ft.Column(
            expand = True,
            spacing = 0,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            controls = [
                header,
                title_banner,
                ft.Container(height = 10),
                podium_container,
                bottom_sheet,
            ],
        )
    )

if __name__ == "__main__":
    ft.run(main)