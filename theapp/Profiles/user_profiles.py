from datetime import datetime, timezone
import firebase_admin
from firebase_admin import auth, credentials, firestore
from pathlib import Path

#Checks if firebase is alr up
if not firebase_admin._apps:
    cred_path = Path(__file__).resolve().parent.parent / "cardioKey.json"
    cred = credentials.Certificate(str(cred_path))
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


def create_profile(email, password, username):
    user_record = auth.create_user(
        email = email,
        password = password,
        display_name = username
    )

    UserId = user_record.uid
    user_ref = db.collection(USERS_COLLECTION).document(UserId)


    profile_data = {
        "uid": UserId,
        "username": username,
        "email": email,
        "avatar_url": None,
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

if __name__ == "__main__":
    test_email = "noa@mailer.com"

    try:
        profile = create_profile(test_email, "PASSWORD123123", "NotNoah F")
        created_uid = profile["uid"]
    except auth.EmailAlreadyExistsError:
        existing_user = auth.get_user_by_email(test_email)
        created_uid = existing_user.uid
        print("User already exists, using existing UID:", created_uid)

    print("Fetched profile:", get_user_profile(created_uid))
    update_user_distance(created_uid, 0.95)
    print("Updated profile:", get_user_profile(created_uid))