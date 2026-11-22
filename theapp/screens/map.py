import logging

import flet as ft
import flet_map as fmap

log = logging.getLogger(f"app.{__name__}")

# Approximate bounds around Carleton University's main campus in Ottawa.
CAMPUS_BOUNDS = fmap.MapLatitudeLongitudeBounds(
    corner_1=fmap.MapLatitudeLongitude(latitude=45.3820, longitude=-75.7048),
    corner_2=fmap.MapLatitudeLongitude(latitude=45.3948, longitude=-75.6868),
)
CAMPUS_CENTER = fmap.MapLatitudeLongitude(latitude=45.3885, longitude=-75.6960)


def map_view() -> ft.Control:
    campus_map = None
    recenter_in_progress = False

    async def keep_camera_on_campus(e):
        nonlocal recenter_in_progress
        if not e.has_gesture or recenter_in_progress:
            return

        latitude = min(max(e.coordinates.latitude, 45.3820), 45.3948)
        longitude = min(max(e.coordinates.longitude, -75.7048), -75.6868)
        if (
            abs(latitude - e.coordinates.latitude) > 0.00001
            or abs(longitude - e.coordinates.longitude) > 0.00001
        ):
            recenter_in_progress = True
            try:
                await campus_map.move_to(
                    destination=fmap.MapLatitudeLongitude(
                        latitude=latitude,
                        longitude=longitude,
                    ),
                    zoom=e.camera.zoom,
                )
            finally:
                recenter_in_progress = False

    campus_map = fmap.Map(
        expand=True,
        initial_center=CAMPUS_CENTER,
        initial_zoom=17,
        initial_camera_fit=fmap.CameraFit(
            bounds=CAMPUS_BOUNDS,
            padding=ft.Padding.all(18),
            min_zoom=14,
            max_zoom=18,
        ),
        min_zoom=14,
        max_zoom=19,
        on_position_change=keep_camera_on_campus,
        layers=[
            fmap.TileLayer(
                url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                user_agent_package_name="carleton-campus-map",
                min_zoom=14,
                max_zoom=19,
                tile_bounds=CAMPUS_BOUNDS,
            ),
            fmap.MarkerLayer(
                markers=[
                    fmap.Marker(
                        coordinates=CAMPUS_CENTER,
                        width=34,
                        height=34,
                        content=ft.Icon(
                            ft.Icons.LOCATION_PIN,
                            color=ft.Colors.RED,
                            size=34,
                        ),
                    )
                ]
            ),
        ],
    )

    map_surface = ft.Stack(
        expand=True,
        controls=[
            campus_map,
            ft.Container(
                right=8,
                bottom=8,
                padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                bgcolor=ft.Colors.with_opacity(0.88, ft.Colors.WHITE),
                border_radius=8,
                content=ft.Text(
                    "© OpenStreetMap contributors",
                    size=10,
                    color=ft.Colors.BLACK,
                ),
            ),
        ],
    )

    log.debug("Built the Carleton campus map view")
    return ft.Column(
        expand=True,
        spacing=12,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        tight=True,
                        spacing=2,
                        controls=[
                            ft.Text(
                                "Campus map",
                                size=23,
                                weight=ft.FontWeight.BOLD,
                                color="#26382C",
                            ),
                            ft.Text(
                                "OpenStreetMap · Carleton University",
                                size=12,
                                color="#647064",
                            ),
                        ],
                    ),
                    ft.Icon(ft.Icons.MAP_OUTLINED, color="#A51C30", size=24),
                ],
            ),
            ft.Container(
                expand=True,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                border_radius=20,
                content=map_surface,
            ),
        ],
    )
