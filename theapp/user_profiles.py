from datetime import datetime, timezone
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"C:\Users\noahw\Documents\Carleton-Cardio\theapp\carleton-cardio-firebase-adminsdk-fbsvc-99fe63f986.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

USERS_COLLECTION = "users"

# user_ref = db.collection("users").document("noah_test_1")
# user_ref.set({
#     "username" : "noah_runs",
#     "avatar_url": None,
#     "total_distance_km": 0.0,
# })
# print("Successfully wrote profile to Firestore!")

# doc = user_ref.get()
# if doc.exists:
#     print("Fetched profile from Firestore: ", doc.to_dict())
# else:
#     print("Document not found.")


def create_new_user_profile(UserId, username, avatar_url):
    user_ref = db.collection(USERS_COLLECTION).document(UserId)
    profile_data = {
        "username": username,
        "avatar_url": avatar_url,
        "total_distance_km": 0.0,
        "created_at": datetime.now(timezone.utc),
    }

    user_ref.set(profile_data)
    print("Profile created for UserId: ", UserId)
    return profile_data

def get_user_profile(UserId):
    doc = db.collection(USERS_COLLECTION).document(UserId).get()
    return doc.to_dict() if doc.exists else None

def update_user_distance(UserId, distance_km):
    user_ref = db.collection(USERS_COLLECTION).document(UserId)
    doc = user_ref.get()
    if not doc.exists:
        print(f"User {UserId} does not exist.")
        return None

    current_distance = doc.to_dict().get("total_distance_km", 0.0)
    new_distance = round(current_distance + distance_km, 2)
    user_ref.update({"total_distance_km": new_distance})
    return new_distance