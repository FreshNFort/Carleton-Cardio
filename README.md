# Carleton-Cardio

A Strava-like app, made for use on Carleton's campus. Built with Python, Flet, and Firebase. Students can track outdoor campus walks, validate activity speeds, and compete on a leaderboard

* **User Profiles & Authentication:** Account registration and profile storage backed by Firebase Authentication and Cloud Firestore (`users` file).

* **Activity Logging & Anti-Cheat:** Logs walk and run distances and validates average speed to filter out biking or driving (`activities` file).

* **Leaderboards:** Ranks users globally by total distance (`total_distance_km`)

* **Cross-Platform UI:** Built with Flet for android and apple compatibility.

## Tech Stack

* **Frontend:** [Flet](https://flet.dev/) (Python)

* **Backend & Database:** Firebase Admin SDK (Cloud Firestore & Firebase Authentication)

* **Package Management:** [uv](https://docs.astral.sh/uv/)