"""Live walking map and session controls."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone

import flet as ft
import flet_geolocator as fg
import flet_map as fm

import styles

from storage import finish_session, load_active_session, load_sessions, save_active_session
from tracking import append_fix, distance_m, format_distance
from screens import home

log = logging.getLogger("app.views.map")

MAROON = "#551414"      # text (matches styles.HOME_PARAGRAPH_TEXT)
MAROON_BTN = "#7C2932"  # accents / buttons (matches styles.RECORD_BUTTON)

# Approximate bounds around Carleton University's main campus in Ottawa.
SOUTH, WEST, NORTH, EAST = 45.3820, -75.7048, 45.3948, -75.6868
CAMPUS_BOUNDS = fm.MapLatitudeLongitudeBounds(
    corner_1=fm.MapLatitudeLongitude(latitude=SOUTH, longitude=WEST),
    corner_2=fm.MapLatitudeLongitude(latitude=NORTH, longitude=EAST),
)
CAMPUS_CENTER = fm.MapLatitudeLongitude(latitude=45.3885, longitude=-75.6960)


def map_view(
    page: ft.Page, *, include_home: bool = True, start_immediately: bool = False
) -> ft.Control:
    prefs = ft.SharedPreferences()
    geolocator = fg.Geolocator(
        configuration=fg.GeolocatorConfiguration(
            accuracy=fg.GeolocatorPositionAccuracy.BEST, distance_filter=0
        )
    )
    for service in (prefs, geolocator):
        if service not in page.services:
            page.services.append(service)
    locations: list[list[float]] = []
    sessions: list[dict] = []
    active_session: dict | None = None
    is_recording = False
    raw_samples = filtered_samples = 0
    recentering = False

    trail = fm.PolylineLayer(polylines=[])
    live_marker = fm.MarkerLayer(markers=[])
    campus_marker = fm.MarkerLayer(
        markers=[
            fm.Marker(
                coordinates=CAMPUS_CENTER,
                width=34,
                height=34,
                content=ft.Icon(ft.Icons.LOCATION_PIN, color=ft.Colors.RED, size=34),
            )
        ]
    )
    tiles = fm.TileLayer(
        url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        user_agent_package_name="carleton-campus-map",
        min_zoom=14,
        max_zoom=19,
        tile_bounds=CAMPUS_BOUNDS,
    )
    map_view = None

    async def keep_camera_on_campus(event):
        nonlocal recentering
        if not event.has_gesture or recentering:
            return
        latitude = min(max(event.coordinates.latitude, SOUTH), NORTH)
        longitude = min(max(event.coordinates.longitude, WEST), EAST)
        if (latitude, longitude) == (event.coordinates.latitude, event.coordinates.longitude):
            return
        recentering = True
        try:
            await map_view.move_to(
                destination=fm.MapLatitudeLongitude(latitude=latitude, longitude=longitude),
                zoom=event.camera.zoom,
            )
        finally:
            recentering = False

    map_view = fm.Map(
        expand=True,
        initial_center=CAMPUS_CENTER,
        initial_zoom=17,
        initial_camera_fit=fm.CameraFit(
            bounds=CAMPUS_BOUNDS, padding=ft.Padding.all(18), min_zoom=14, max_zoom=18
        ),
        min_zoom=14,
        max_zoom=19,
        on_position_change=keep_camera_on_campus,
        layers=[tiles, trail, campus_marker, live_marker],
    )
    map_surface = ft.Stack(
        expand=True,
        controls=[
            map_view,
            ft.Container(
                right=8,
                bottom=8,
                padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                bgcolor=ft.Colors.with_opacity(0.88, ft.Colors.WHITE),
                border_radius=8,
                content=ft.Text("© OpenStreetMap contributors", size=10, color=ft.Colors.BLACK),
            ),
        ],
    )

    distance_label = ft.Text("0 m", size=28, weight=ft.FontWeight.BOLD, color=MAROON)
    points_label = ft.Text("0 points", color=MAROON)
    status_label = ft.Text("Ready when you are", color=MAROON)
    history_column = ft.Column(spacing=4)
    record_button = ft.Button(
        content=ft.Row(
            controls=[ft.Icon(ft.Icons.FIBER_MANUAL_RECORD, size=18), ft.Text("Start walk")],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        color=ft.Colors.WHITE,
        bgcolor=MAROON_BTN,
    )

    def refresh_route() -> None:
        points = [fm.MapLatitudeLongitude(latitude=lat, longitude=lon) for lat, lon in locations]
        trail.polylines = (
            [fm.PolylineMarker(coordinates=points, color=MAROON_BTN, stroke_width=6)]
            if len(points) > 1 else []
        )
        live_marker.markers = (
            [fm.Marker(
                coordinates=points[-1],
                content=ft.Icon(ft.Icons.LOCATION_ON, color=MAROON_BTN, size=34),
                width=38,
                height=38,
            )]
            if points else []
        )
        distance_label.value = format_distance(
            float(active_session.get("distance_m", 0)) if active_session else 0
        )
        points_label.value = f"{raw_samples} fixes · {len(locations)} kept · {filtered_samples} filtered"
        map_view.layers = [tiles, trail, campus_marker, live_marker]

    def refresh_history() -> None:
        history_column.controls = [
            ft.Row(
                controls=[
                    ft.Icon(ft.Icons.DIRECTIONS_WALK, size=18),
                    ft.Text(
                        f"{session.get('date_label', 'Walk')} · "
                        f"{format_distance(float(session.get('distance_m', 0)))}",
                        expand=True,
                     color=MAROON),
                    ft.Text(f"{len(session.get('coordinates', []))} pts", color=MAROON),
                ]
            )
            for session in reversed(sessions[-4:])
        ] or [ft.Text("Completed walks will appear here.", color=MAROON)]

    def update_button() -> None:
        label, icon, color = (
            ("Stop walk", ft.Icons.STOP, ft.Colors.RED_700)
            if is_recording else
            ("Resume walk", ft.Icons.PLAY_ARROW, MAROON_BTN)
            if active_session else
            ("Start walk", ft.Icons.FIBER_MANUAL_RECORD, MAROON_BTN)
        )
        record_button.content = ft.Row(
            controls=[ft.Icon(icon, size=18), ft.Text(label)],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        record_button.bgcolor = color

    async def save_point(lat: float, lon: float, accuracy: float | None) -> None:
        nonlocal raw_samples, filtered_samples
        candidate = [lat, lon]
        previous = locations[-1] if locations else None
        raw_samples += 1
        accepted = append_fix(locations, candidate)
        accuracy_text = f" · ±{accuracy:.0f} m" if accuracy is not None else ""
        if accepted:
            if previous is not None:
                active_session["distance_m"] += distance_m(previous, candidate)
            status_label.value = f"GPS {lat:.5f}, {lon:.5f}{accuracy_text} · route updated"
            log.debug("accepted GPS fix %.6f, %.6f%s", lat, lon, accuracy_text)
        else:
            filtered_samples += 1
            status_label.value = f"GPS {lat:.5f}, {lon:.5f}{accuracy_text} · nearby fix filtered"
            log.debug("filtered GPS fix %.6f, %.6f%s", lat, lon, accuracy_text)
        active_session["last_fix_at"] = datetime.now(timezone.utc).isoformat()
        await save_active_session(prefs, active_session)
        refresh_route()
        try:
            await map_view.center_on(
                point=fm.MapLatitudeLongitude(latitude=lat, longitude=lon), zoom=17
            )
        except Exception:
            log.debug("Map camera could not center on GPS fix", exc_info=True)
        page.update()

    async def process_fix(fix: fg.GeolocatorPosition) -> None:
        if not is_recording:
            return
        if fix.latitude is None or fix.longitude is None:
            status_label.value = "Waiting for a GPS fix…"
            page.update()
            return
        await save_point(
            float(fix.latitude),
            float(fix.longitude),
            float(fix.accuracy) if fix.accuracy is not None else None,
        )

    async def on_position_change(event: fg.GeolocatorPositionChangeEvent) -> None:
        log.debug("live GPS position event received")
        await process_fix(event.position)

    geolocator.on_position_change = on_position_change

    async def start_recording() -> None:
        nonlocal active_session, is_recording, locations, raw_samples, filtered_samples
        if is_recording:
            is_recording = False
            if active_session:
                active_session["last_fix_at"] = datetime.now(timezone.utc).isoformat()
                await save_active_session(prefs, active_session)
                status_label.value = "Walk paused — tap resume to continue"
            update_button()
            page.update()
            return
        try:
            service_enabled = await geolocator.is_location_service_enabled()
            permission = await geolocator.get_permission_status()
            allowed = (fg.GeolocatorPermissionStatus.WHILE_IN_USE, fg.GeolocatorPermissionStatus.ALWAYS)
            if permission not in allowed:
                permission = await geolocator.request_permission()
            if permission not in allowed:
                status_label.value = "Allow location access in device settings to track."
                page.update()
                return
            if not service_enabled:
                status_label.value = "Turn on location services to start a walk."
                page.update()
                return
        except Exception as error:
            log.warning("Could not start location service: %s", error)
            status_label.value = "Location is available in the installed mobile app."
            page.update()
            return

        try:
            current_fix = await geolocator.get_current_position()
        except Exception as error:
            log.warning("Could not get a location before starting: %s", error)
            status_label.value = "Could not get your location. Try again outdoors."
            page.update()
            return
        if current_fix.latitude is None or current_fix.longitude is None:
            status_label.value = "Waiting for a GPS fix before starting."
            page.update()
            return
        latitude, longitude = float(current_fix.latitude), float(current_fix.longitude)
        if not (SOUTH <= latitude <= NORTH and WEST <= longitude <= EAST):
            message = "Walk sessions can only start on Carleton's main campus."
            status_label.value = message
            page.show_dialog(ft.SnackBar(content=ft.Text(message)))
            page.update()
            return

        raw_samples = filtered_samples = 0
        if active_session is None:
            now = datetime.now(timezone.utc)
            active_session = {
                "started_at": now.isoformat(),
                "date_label": now.astimezone().strftime("%b %d, %I:%M %p"),
                "coordinates": [],
                "distance_m": 0.0,
            }
            locations = active_session["coordinates"]
        is_recording = True
        status_label.value = "Getting your location…"
        update_button()
        await save_active_session(prefs, active_session)
        page.update()
        page.run_task(process_fix, current_fix)

    async def stop_recording() -> None:
        nonlocal active_session, locations, sessions, is_recording
        if not active_session:
            return
        is_recording = False
        ended = datetime.now(timezone.utc)
        active_session["ended_at"] = ended.isoformat()
        try:
            started = datetime.fromisoformat(active_session["started_at"])
            active_session["duration_s"] = max(0, int((ended - started).total_seconds()))
        except (TypeError, ValueError):
            active_session["duration_s"] = 0
        sessions = await finish_session(prefs, active_session)
        active_session = None
        locations = []
        refresh_history()
        refresh_route()
        status_label.value = "Walk saved on this device"
        update_button()
        page.update()

    async def handle_button() -> None:
        await stop_recording() if is_recording else await start_recording()

    record_button.on_click = handle_button
    transition = ft.Animation(duration=420, curve=ft.AnimationCurve.EASE_IN_OUT_CUBIC)
    home_status = ft.Text("", visible=False, color=ft.Colors.RED_700)

    async def start_from_home():
        home_status.visible = False
        await start_recording()
        if is_recording:
            home_screen.offset, map_screen.offset = ft.Offset(x=-1.1, y=0), ft.Offset(x=0, y=0)
        else:
            home_status.value = status_label.value
            home_status.visible = True
        page.update()

    home_screen = home.home_view(start_from_home) if include_home else None
    if home_screen is not None:
        home_screen.animate_offset = transition
    header = ft.Row(
        controls=[
            ft.Column(
                spacing=2,
                controls=[
                    ft.Text("Trailkeeper", size=27, weight=ft.FontWeight.BOLD, color=MAROON),
                    ft.Text("OpenStreetMap · Carleton University", color=MAROON),
                ],
                expand=True,
            ),
            ft.Icon(ft.Icons.DIRECTIONS_WALK, size=30),
        ]
    )
    stats = ft.Row(
        controls=[
            ft.Column(
                spacing=2,
                controls=[ft.Text("SESSION DISTANCE", color=MAROON), distance_label],
                expand=True,
            ),
            ft.Column(
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.END,
                controls=[ft.Text("GPS SAMPLES", color=MAROON), points_label],
            ),
        ]
    )
    actions = ft.Row(
        controls=[ft.Container(content=status_label, expand=True), record_button],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    history = ft.Container(
        content=ft.Column(
            spacing=6,
            controls=[
                ft.Text("RECENT WALKS", weight=ft.FontWeight.BOLD, color=MAROON),
                history_column,
                ft.Text(
                    "Background GPS may pause when iOS or Android suspends the app.", size=11
                , color=MAROON),
            ],
        ),
        padding=12,
        border_radius=16,
        bgcolor="#FFF4F5",
    )
    map_screen = ft.SafeArea(
        expand=True,
        offset=ft.Offset(x=1.1 if include_home else 0, y=0),
        animate_offset=transition,
        content=ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=12,
            controls=[
                header,
                ft.Container(
                    content=map_surface,
                    expand=True,
                    border_radius=20,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                ),
                stats,
                actions,
                history,
            ],
        ),
    )
    root_controls = [map_screen]
    if home_screen is not None:
        root_controls.extend(
            [home_screen, ft.Container(left=16, right=16, bottom=16, content=home_status)]
        )
    root = ft.Stack(
        expand=True,
        fit=ft.StackFit.EXPAND,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        controls=root_controls,
    )

    async def load_saved_walks() -> None:
        nonlocal sessions, active_session, locations
        sessions = await load_sessions(prefs)
        active_session = await load_active_session(prefs)
        if active_session:
            cleaned: list[list[float]] = []
            for fix in active_session.get("coordinates", []):
                if not cleaned or distance_m(cleaned[-1], fix) > 0.05:
                    cleaned.append([float(fix[0]), float(fix[1])])
            locations = cleaned
            active_session["coordinates"] = locations
            active_session["distance_m"] = sum(
                distance_m(locations[i - 1], locations[i])
                for i in range(1, len(locations))
            )
            await save_active_session(prefs, active_session)
            status_label.value = "Saved walk found — resume recording when ready"
        refresh_history()
        refresh_route()
        update_button()
        page.update()
        if start_immediately:
            await start_recording()

    page.run_task(load_saved_walks)
    return root