import flet as ft
import styles


def stat_box(title: str, value: str) -> ft.Container:
    return ft.Container(
        col={"xs": 6, "md": 3},
        **styles.BOX_STYLE,
        height=105,
        gradient=styles.CARD_GRADIENT1,
        shadow=styles.CARD_SHADOW,
        content=ft.Column(
            [
                ft.Text(title, **styles.BOX_TEXT_STYLE1),
                ft.Text(value, **styles.BOX_TEXT_STYLE1, size=24, weight=ft.FontWeight.BOLD),
            ],
        ),
    )


def home_view(on_record=None) -> ft.Control:
    # Controls are built inside the function so every call gets fresh instances
    # (Flet controls can't safely be shared between rebuilt screens).
    header = ft.Row(
        controls=[
            ft.Container(
                padding=ft.Padding.only(top=25),
                content=ft.Text(
                    "Welcome!",
                    style=ft.TextStyle(
                        size=32,
                        shadow=styles.HEADING_SHADOW,
                        font_family="Segoe UI",
                        **styles.HEADING1_TEXT_STYLE,
                    ),
                ),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    two_boxes_layout = ft.ResponsiveRow(
        spacing=10,
        run_spacing=10,
        controls=[
            stat_box("Distance:", "3.2 km"),
            stat_box("Time Spent:", "2.5 hrs"),
        ],
    )

    leaderboard_button = ft.Button(
        style=styles.LEADERBOARD_BUTTON,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("View Leaderboard", size=14),
                ft.Icon(ft.Icons.LEADERBOARD_ROUNDED, color="#FFE8EA"),
            ],
        ),
    )

    leaderboard_box = ft.Container(
        col={"xs": 12, "md": 12},
        **styles.BOX_STYLE,
        height=200,
        gradient=styles.CARD_GRADIENT2,
        shadow=styles.CARD_SHADOW,
        content=ft.Column(
            [
                ft.Text("Leaderboard Position:", **styles.BOX_TEXT_STYLE2, size=20, weight=ft.FontWeight.W_600),
                ft.Text("3rd", **styles.BOX_TEXT_STYLE2, size=32, weight=ft.FontWeight.BOLD),
                ft.Text("You're x points behind y!", **styles.BOX_TEXT_STYLE2),
                leaderboard_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    record_button = ft.Button(
        style=styles.RECORD_BUTTON,
        on_click=on_record,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("Record", size=18),
                ft.Icon(ft.Icons.ADJUST_OUTLINED, color="#FFE8EA"),
            ],
        ),
    )

    return ft.Column(
        scroll=ft.ScrollMode.HIDDEN,
        alignment=ft.Alignment(0, -1),
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        expand=True,
        controls=[
            ft.SafeArea(
                content=ft.ResponsiveRow(
                    controls=[
                        header,
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Text(
                                        "Explore your dashboard", size=16, **styles.HOME_PARAGRAPH_TEXT
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Container(
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                                controls=[two_boxes_layout, leaderboard_box],
                            ),
                        ),
                        ft.Container(
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                                controls=[
                                    ft.Text("Start a new session?", size=16, **styles.HEADING2_TEXT_STYLE),
                                    record_button,
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )