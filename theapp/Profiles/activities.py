from datetime import datetime, timezone
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path


# Key file lives in the theapp folder, one level above this Profiles folder.
# Building the path from this file's location means it works from any launch folder.
KEY_PATH = Path(__file__).resolve().parent.parent / "cardioKey.json"

# Checks if firebase is already up - updated to not be stuck on one file path
if not firebase_admin._apps:
    cred = credentials.Certificate(str(KEY_PATH))
    firebase_admin.initialize_app(cred)

"""
#Checks if firebase is alr up
if not firebase_admin._apps:
    cred = credentials.Certificate(
        "./theapp/cardioKey.json"
    )
    firebase_admin.initialize_app(cred)

"""

db = firestore.client()

USERS_COLLECTION = "users"
ACTIVITIES_COLLECTION = "activities"

# Maximum valid speed in km/h (Hopefully noones running faster than this)
MAX_SPEED_KMH = 20.0


def log_activity(user_id: str, distance_meters: float, duration_seconds: float, is_tunnel: bool = False,) -> dict | None:
    """Logs a walk/run session, validates speed, and updates user distance if valid."""
    if duration_seconds <= 0 or distance_meters < 0:
        print("ERROR: Invalid distance or duration")
        return None

    user_ref = db.collection(USERS_COLLECTION).document(user_id)
    user_doc = user_ref.get()
    if not user_doc.exists:
        print(f"ERROR: User {user_id} not found.")
        return None

    #Calculate speed in km/h: (meters / seconds) * 3.6
    speed_kmh = round((distance_meters / duration_seconds) * 3.6, 2)
    is_valid = speed_kmh <= MAX_SPEED_KMH
    distance_km = round(distance_meters / 1000.0, 3)

    #Builds the activity document
    activity_data = {
        "user_id": user_id,
        "distance_meters": distance_meters,
        "distance_km": distance_km,
        "duration_seconds": duration_seconds,
        "avg_speed_kmh": speed_kmh,
        "is_tunnel": is_tunnel,
        "valid": is_valid,
        "created_at": datetime.now(timezone.utc),
    }

    #Saves to Firestore activities collection (auto-generates an activity ID)
    _, activity_ref = db.collection(ACTIVITIES_COLLECTION).add(activity_data)
    activity_data["id"] = activity_ref.id

    #Only add to total_distance_km if the speed check passes
    if is_valid:
        current_total = user_doc.to_dict().get("total_distance_km", 0.0)
        new_total = round(current_total + distance_km, 2)
        user_ref.update({"total_distance_km": new_total})
        print(f"Valid walk logged ({speed_kmh} km/h). New user total: {new_total} km")
    else:
        print(f"Activity flagged as invalid ({speed_kmh} km/h exceeds {MAX_SPEED_KMH} km/h). Distance not added.")

    return activity_data


def get_user_activities(user_id: str, limit: int = 10) -> list[dict]:
    """Fetches a user's recent activity history."""
    docs = (
        db.collection(ACTIVITIES_COLLECTION)
        .where("user_id", "==", user_id)
        .limit(limit)
        .stream()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

#NEWW
def get_user_totals(user_id: str) -> dict:
    """Returns all-time distance (km) and time (hours) across a user's valid activities."""
    docs = (
        db.collection(ACTIVITIES_COLLECTION)
        .where("user_id", "==", user_id)
        .where("valid", "==", True)
        .stream()
    )

    total_km = 0.0
    total_seconds = 0.0
    for doc in docs:
        data = doc.to_dict()
        total_km += data.get("distance_km", 0.0)
        total_seconds += data.get("duration_seconds", 0.0)

    return {
        "distance_km": round(total_km, 1),
        "time_hours": round(total_seconds / 3600, 1),
    }

if __name__ == "__main__":
    test_uid = "ActivityTester"

    #Tests normal tunnel walk (500 meters in 360 seconds = 5.0 km/h)
    print("Logging Valid Tunnel Walk")
    log_activity(test_uid, distance_meters=500, duration_seconds=360, is_tunnel=True)

    #tests driving/biking speed 2000 meters in 180 seconds = 40.0 km/h -> Invalid)
    print("\nLogging Speed Violation")
    log_activity(test_uid, distance_meters=2000, duration_seconds=180, is_tunnel=False)

    #Prints the user_id attributes
    print("\nRecent Activities")
    for act in get_user_activities(test_uid):
        print(act)