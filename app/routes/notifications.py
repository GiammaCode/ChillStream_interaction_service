from datetime import datetime

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

@notifications_bp.route("/<string:userId>/profiles/<string:profileId>/notifications", methods=["POST"])
def add_notification(userId, profileId):
    """
    Add a new notification for a specific user profile.

    Request Body:
        JSON: { "sender_id": "65c2e8a67f3b5b8c21e4d9f2", "text": "New friend request!" }

    Returns:
        Response: Success message or error message.
    """
    data = request.json

    # Creazione della notifica
    notification_data = {
        "sender_id": str(data.get("sender_id")),  # ID del mittente
        "receiver_id": profileId,  # ID del destinatario (profilo)
        "text": data.get("text", ""),  # Testo della notifica
        "timestamp": datetime.utcnow().isoformat()  # Timestamp attuale
    }

    result = mongo.db.notifications.insert_one(notification_data)
    notification_id = str(result.inserted_id)

    return jsonify({"message": "Notification added", "notification_id": notification_id}), 201

@notifications_bp.route("/<string:userId>/profiles/<string:profileId>/notifications/<string:notificationId>", methods=["DELETE"])
def delete_notification(userId, profileId, notificationId):
    """
    Delete a specific notification from a user's profile.

    Args:
        userId (str): The unique ID of the user.
        profileId (str): The unique ID of the profile.
        notificationId (str): The unique ID of the notification.

    Returns:
        Response: Success or error message.
    """

    try:
        # Controllo se gli ID sono validi
        notification_object_id = ObjectId(notificationId)
    except Exception as e:
        return jsonify({"error": "Invalid ID format"}), 400


    # Controllo se la notifica esiste
    notification = mongo.db.notifications.find_one({"_id": notification_object_id, "receiver_id": profileId})
    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    # Elimina la notifica dal database
    mongo.db.notifications.delete_one({"_id": notification_object_id})

    return jsonify({"message": "Notification deleted"}), 204
