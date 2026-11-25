# CHANGELOG.md

## 1.0.0 (unreleased)
Fixed:
- Leaderboard podium truncating full names on spaces[cite: 3]
- Home screen showing hardcoded distance and rank instead of live user stats[cite: 3]
Added:
- Live Firestore profile, distance, and rank integration across Home, Leaderboard, and Profile screens[cite: 3, 7]
- GPS walk recording sync to automatically log sessions and update user distance in Firestore on completion[cite: 2]
Chore:
- Added `README.md` with project structure and local `uv` setup instructions[cite: 3]

## 0.3.0 (2026-11-21)
Fixed:
- Resolved relative credential path issues across macOS and Windows using `pathlib`[cite: 6]
Added:
- Activity logging (`activities.py`) with average speed validation (`<= 20.0 km/h`)[cite: 6]
- Global leaderboard queries (`leaderboard.py`) supporting `All-Time`, `Weekly`, and `Daily` timeframes[cite: 6]
- Leaderboard UI wired to live Firestore rankings[cite: 6]
Chore:
- Excluded compiled Python cache (`__pycache__/`, `*.pyc`) from version control[cite: 6]

## 0.2.0 (2026-11-08)
Added:
- User profile management (`user_profiles.py`) with Firebase Authentication registration and Firestore persistence[cite: 6]
- Username prefix search for finding users[cite: 6]
Chore:
- Configured `.gitignore` to exclude Firebase service account keys[cite: 6]

## 0.1.0 (2026-10-21)
Added:
- Initialized project dependencies (`flet`, `firebase-admin`) with `uv`[cite: 3, 5]
- Established Cloud Firestore connection and verified initial read/write operations[cite: 6]