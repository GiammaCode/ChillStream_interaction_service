from datetime import datetime
from bson import ObjectId

class Notification:
    """
    Represents a notification between users.
    """

    def __init__(self, notification_id ,senderNickname,ricever_id, text, timestamp):
        """
        Initializes a Notification instance.

        Args:
            sender_id (str): The unique MongoDB ObjectId of the sender.
            text (str): The content of the notification.
            timestamp (str, optional): The time the notification was created.
        """
        self.notification_id = str(notification_id) if notification_id else None
        self.senderNickname= str(senderNickname)
        self.ricever_id = str(ricever_id)
        self.isChecked= False
        self.text = text
        self.timestamp = timestamp if timestamp else datetime.utcnow().isoformat()

    def to_dict(self):
        """
        Converts the Notification instance into a dictionary.
        """
        return {
            "_id": self.notification_id,
            "senderNickname": self.senderNickname,
            "ricever_id":self.ricever_id,
            "isChecked":self.isChecked,
            "text": self.text,
            "timestamp": self.timestamp
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Notification instance from a dictionary.
        """
        return Notification(
            notification_id=data.get("_id"),
            senderNickname=data.get("senderNickname"),
            ricever_id = data.get("ricever_id"),
            text=data.get("text"),
            timestamp=data.get("timestamp")
        )
