import firebase_admin
from firebase_admin import credentials, messaging
import os
import json

class NotificationManager:
    _instance = None

    def __init__(self):
        # We check if already initialized to avoid duplicate app errors
        if not firebase_admin._apps:
            try:
                # In production, path to serviceAccountKey.json from env
                # For now, we provide a placeholder setup
                cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT")
                if cred_path and os.path.exists(cred_path):
                    cred = credentials.Certificate(cred_path)
                    firebase_admin.initialize_app(cred)
                    print("Firebase Admin SDK initialized.")
                else:
                    print("FIREBASE_SERVICE_ACCOUNT not found. Push notifications disabled.")
            except Exception as e:
                print(f"Error initializing Firebase: {e}")

    def send_alert(self, title: str, body: str, topic: str = "doctor_alerts"):
        """
        Sends a notification to a specific topic (e.g., 'doctor_alerts')
        """
        if not firebase_admin._apps:
            print("Cannot send notification: Firebase not initialized.")
            return

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            topic=topic,
            data={
                "click_action": "FLUTTER_NOTIFICATION_CLICK",
                "status": "critical"
            }
        )

        try:
            response = messaging.send(message)
            print(f"Successfully sent message: {response}")
        except Exception as e:
            print(f"Error sending message: {e}")

# Global instance
notifier = NotificationManager()
