import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

#Checks if firebase is alr up
if not firebase_admin._apps:
    cred_path = Path(__file__).resolve().parent.parent / "cardioKey.json"
    cred = credentials.Certificate(str(cred_path))
    firebase_admin.initialize_app(cred)

db = firestore.client()
USERS_COLLECTION = "users"

def get_leaderboard():
    documents = (db.collection(USERS_COLLECTION).order_by("total_distance_km", direction = firestore.Query.DESCENDING).limit(10).stream())

    leaderboard = []
    rank = 1

    for doc in documents:
        data = doc.to_dict()
        entry = {
            "rank": rank,
            "uid": doc.id,
            "username": data.get("username", "Unknown"),
            "total_distance_km": round(data.get("total_distance_km", 0.0), 2)
        }

        leaderboard.append(entry)
        rank = rank + 1

    return leaderboard

if __name__ == "__main__":
    print("Leaderboard")
    top_users = get_leaderboard()

    for user in top_users:
        print(user["rank"], user["username"], user["total_distance_km"], "km")