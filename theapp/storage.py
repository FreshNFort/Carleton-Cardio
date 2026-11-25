"""Local session persistence using Flet SharedPreferences."""

from __future__ import annotations

import json

SESSIONS_KEY = "trailkeeper.sessions"
ACTIVE_KEY = "trailkeeper.active"


async def load_sessions(preferences) -> list[dict]:
    value = await preferences.get(SESSIONS_KEY)
    if not value:
        return []
    try:
        sessions = json.loads(value)
        return sessions if isinstance(sessions, list) else []
    except (TypeError, json.JSONDecodeError):
        return []


async def load_active_session(preferences) -> dict | None:
    value = await preferences.get(ACTIVE_KEY)
    if not value:
        return None
    try:
        session = json.loads(value)
        return session if isinstance(session, dict) else None
    except (TypeError, json.JSONDecodeError):
        return None


async def save_active_session(preferences, session: dict) -> None:
    await preferences.set(ACTIVE_KEY, json.dumps(session))


async def finish_session(preferences, session: dict) -> list[dict]:
    sessions = await load_sessions(preferences)
    sessions.append(session)
    sessions = sessions[-100:]
    await preferences.set(SESSIONS_KEY, json.dumps(sessions))
    await preferences.remove(ACTIVE_KEY)
    return sessions
