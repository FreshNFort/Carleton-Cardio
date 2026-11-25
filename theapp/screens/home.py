import flet as ft
import styles
from Profiles.activities import get_user_totals
from Profiles.user_profiles import get_user_profile
from Profiles.leaderboard import get_leaderboard

USER_ID = "noah fortin"


def stat_box(title: str, value: str) -> ft.Container:
    return ft.Container(
        col={"xs": 12, "md": 12},
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


def load_dashboard_data() -> dict:
    """Fetch everything the home screen needs. Falls back to defaults if Firebase fails."""
    data = {
        "username": None,
        "distance_km": 0.0,
        "time_hours": 0.0,
        "rank": "-",
        "rank_note": "Log a walk to join the leaderboard!",
    }
    try:
        profile = get_user_profile(USER_ID) or {}
        data["username"] = profile.get("username")
        data["distance_km"] = profile.get("total_distance_km", 0.0)
    except Exception as error:
        print(f"Could not load profile: {error}")

    try:
        data["time_hours"] = get_user_totals(USER_ID).get("time_hours", 0.0)
    except Exception as error:
        print(f"Could not load activity totals: {error}")

    try:
        board = get_leaderboard()
        for i, entry in enumerate(board):
            if entry["uid"] == USER_ID:
                data["rank"] = f"#{entry['rank']}"
                if i == 0:
                    data["rank_note"] = "You're in the lead!"
                else:
                    ahead = board[i - 1]
                    gap = round(ahead["total_distance_km"] - entry["total_distance_km"], 2)
                    data["rank_note"] = f"You're {gap} km behind {ahead['username']}!"
                break
    except Exception as error:
        print(f"Could not load leaderboard: {error}")

    return data


def home_view(on_record=None, on_leaderboard=None) -> ft.Control:    # Controls are built inside the function so every call gets fresh instances
    # (Flet controls can't safely be shared between rebuilt screens).
    info = load_dashboard_data()
    welcome = f"Welcome\n{info['username']}!" if info["username"] else "Welcome!"

    header = ft.Container(
        padding=ft.Padding.only(top=25),
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            welcome,
            text_align=ft.TextAlign.CENTER,
            style=ft.TextStyle(
                size=28,
                shadow=styles.HEADING_SHADOW,
                font_family="Segoe UI",
                **styles.HEADING1_TEXT_STYLE,
            ),
        ),
    )

    two_boxes_layout = ft.ResponsiveRow(
        spacing=10,
        run_spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            stat_box("Distance:", f"{info['distance_km']} km"),
        ],
    )

    leaderboard_button = ft.Button(
        style=styles.LEADERBOARD_BUTTON,
        on_click=on_leaderboard,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("View Leaderboard", size=14),
                ft.Icon(ft.Icons.LEADERBOARD_ROUNDED, color="#FFEAD3"),
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
                ft.Text(info["rank"], **styles.BOX_TEXT_STYLE2, size=32, weight=ft.FontWeight.BOLD),
                ft.Text(info["rank_note"], **styles.BOX_TEXT_STYLE2),
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
                ft.Icon(ft.Icons.ADJUST_OUTLINED, color="#FFEAD3"),
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
                    #width=100,
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