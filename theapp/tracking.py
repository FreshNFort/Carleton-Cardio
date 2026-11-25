"""Walking-session calculations and GPS-jitter filtering."""

from __future__ import annotations

import math
from typing import Sequence

EARTH_RADIUS_M = 6_371_000
JITTER_RADIUS_M = 2.0


def distance_m(a: Sequence[float], b: Sequence[float]) -> float:
    """Return the great-circle distance between two latitude/longitude pairs."""
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1
    haversine = (
        math.sin(d_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    )
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(min(1.0, haversine)))


def should_discard_latest(
    recorded: Sequence[Sequence[float]],
    candidate: Sequence[float],
    radius_m: float = JITTER_RADIUS_M,
) -> bool:
    """Reject the new fix when it is within the radius of any recorded fix."""
    nearby_prior_fixes = sum(
        distance_m(point, candidate) <= radius_m for point in recorded
    )
    return nearby_prior_fixes + 1 >= 2


def append_fix(
    recorded: list[list[float]], candidate: Sequence[float]
) -> bool:
    """Append a fix unless another recording is already within 2 meters."""
    point = [float(candidate[0]), float(candidate[1])]
    if should_discard_latest(recorded, point):
        return False
    recorded.append(point)
    return True


def format_distance(meters: float) -> str:
    if meters >= 1000:
        return f"{meters / 1000:.2f} km"
    return f"{meters:.0f} m"
