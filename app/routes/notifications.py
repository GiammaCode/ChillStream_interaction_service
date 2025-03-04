from datetime import datetime
from flask import Blueprint, request, jsonify
from bson import ObjectId
from services.db import mongo

# Creazione del Blueprint per le notifiche
notifications_bp = Blueprint("notifications", __name__)

# 🔹 GET: Recupera tutte le notifiche per un profilo specifico
@notifications_bp.route("/<string:userId>/profiles/<string:profileId>/notifications", methods=["GET"])
def get_notifications(userId, profileId):
    """
    Retrieve all notifications where profileId matches ricever_id.
    """
    notifications = list(mongo.db.notifications.find({"ricever_id": profileId}))

    for notification in notifications:
        notification["_id"] = str(notification["_id"])  # Converti ObjectId in stringa

    return jsonify(notifications), 200


# 🔹 GET: Recupera una singola notifica
@notifications_bp.route("/<string:userId>/profiles/<string:profileId>/notifications/<string:notificationId>", methods=["GET"])
def get_single_notification(userId, profileId, notificationId):
    """
    Retrieve a specific notification for a user's profile.
    """
    try:
        notification_object_id = ObjectId(notificationId)
    except Exception:
        return jsonify({"error": "Invalid notification ID format"}), 400

    notification = mongo.db.notifications.find_one({"_id": notification_object_id, "ricever_id": profileId})

    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    notification["_id"] = str(notification["_id"])  # Converti ObjectId in stringa
    return jsonify(notification), 200


# 🔹 POST: Aggiunge una nuova notifica
@notifications_bp.route("/<string:userId>/profiles/<string:profileId>/notifications", methods=["POST"])
def add_notification(userId, profileId):
    """
    Add a notification for a specific user profile.
    """
    data = request.json
    required_fields = ["senderNickname", "text"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    new_notification = {
        "senderNickname": data["senderNickname"],
        "ricever_id": profileId,  # Assicuriamoci che la notifica sia per questo profilo
        "text": data["text"],
        "isChecked": False,
        "timestamp": datetime.utcnow().isoformat(),
    }

    result = mongo.db.notifications.insert_one(new_notification)
    new_notification["_id"] = str(result.inserted_id)

    return jsonify(new_notification), 201


# 🔹 PUT: Aggiorna una notifica
@notifications_bp.route("/<string:userId>/profiles/<string:profileId>/notifications/<string:notificationId>", methods=["PUT"])
def update_notification(userId, profileId, notificationId):
    """
    Update a specific notification for a user's profile.
    """
    try:
        notification_object_id = ObjectId(notificationId)
    except Exception:
        return jsonify({"error": "Invalid notification ID format"}), 400

    data = request.json
    allowed_fields = ["text", "isChecked"]

    if not any(field in data for field in allowed_fields):
        return jsonify({"error": "No valid fields to update"}), 400

    update_data = {field: data[field] for field in allowed_fields if field in data}

    result = mongo.db.notifications.update_one(
        {"_id": notification_object_id, "ricever_id": profileId},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Notification not found"}), 404

    return jsonify({"message": "Notification updated successfully"}), 200


# 🔹 DELETE: Elimina una notifica
@notifications_bp.route("/<string:userId>/profiles/<string:profileId>/notifications/<string:notificationId>", methods=["DELETE"])
def delete_notification(userId, profileId, notificationId):
    """
    Delete a specific notification from a user's profile.
    """
    try:
        notification_object_id = ObjectId(notificationId)
    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400

    notification = mongo.db.notifications.find_one({"_id": notification_object_id, "ricever_id": profileId})

    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    mongo.db.notifications.delete_one({"_id": notification_object_id})
    return jsonify({"message": "Notification deleted"}), 204
