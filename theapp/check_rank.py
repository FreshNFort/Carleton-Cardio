from collections import defaultdict
from Profiles.activities import db, USERS_COLLECTION, ACTIVITIES_COLLECTION

# Which user_id values appear in activities, with counts and valid totals
counts = defaultdict(lambda: {"activities": 0, "valid": 0, "valid_km": 0.0})

for doc in db.collection(ACTIVITIES_COLLECTION).stream():
    data = doc.to_dict()
    entry = counts[data.get("user_id")]
    entry["activities"] += 1
    if data.get("valid"):
        entry["valid"] += 1
        entry["valid_km"] += data.get("distance_km", 0.0)

user_ids = {doc.id for doc in db.collection(USERS_COLLECTION).stream()}

print("user_id values in the activities collection:")
for uid, info in counts.items():
    in_users = "yes" if uid in user_ids else "NO"
    print(
        f"  {uid!r}: {info['activities']} activities, "
        f"{info['valid']} valid, {round(info['valid_km'], 2)} km valid | "
        f"has a users document: {in_users}"
    )