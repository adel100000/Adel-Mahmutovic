from datetime import datetime, timezone
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase safe initialization
if not firebase_admin._apps:
    cred = credentials.Certificate("studyai-5ea51-firebase-adminsdk-fbsvc-dff3288e0c.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://studyai-5ea51-default-rtdb.firebaseio.com"
    })

fs = firestore.client()

def save_to_history(entry: dict):
    """Flexible history saver — saves flat dict into 'history' collection."""
    entry["timestamp"] = datetime.now(timezone.utc)
    fs.collection("history").add(entry)
