from flask import Blueprint, request, jsonify
from bson import ObjectId
from services.db import mongo

# Creazione del Blueprint per le notifiche
notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/<string:userId>/profiles/<string:profileId>/notifications", methods=["GET"])
def get_notifications(userId, profileId):
    """
    Retrieve all notifications for a specific user profile.

    Args:
        userId (str): The unique MongoDB ObjectId of the user.
        profileId (str): The unique MongoDB ObjectId of the profile.

    Returns:
        Response: A JSON list of notifications or an error message.
    """
    # Recupera tutte le notifiche ricevute dal profilo
    notifications = list(mongo.db.notifications.find({"receiver_id": profileId}))

    # Converti gli ObjectId in stringhe per compatibilità JSON
    for notification in notifications:
        notification["_id"] = str(notification["_id"])
        notification["sender_id"] = str(notification["sender_id"])
        notification["receiver_id"] = str(notification["receiver_id"])

    return jsonify({"profile_id": profileId, "notifications": notifications}), 200
