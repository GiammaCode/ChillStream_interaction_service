from datetime import datetime

from flask import Blueprint, request, jsonify
from bson import ObjectId
from services.db import mongo

# Creazione del Blueprint per le notifiche
notifications_bp = Blueprint("notifications", __name__)


import requests
from flask import Blueprint, request, jsonify
from services.db import mongo

# Define the Blueprint for notifications
notifications_bp = Blueprint("notifications", __name__)

@notifications_bp.route("/<string:userId>/profiles/<string:profileId>/notifications", methods=["GET"])
def get_notifications(userId, profileId):
    """
    Retrieve all notifications for a specific user profile.

    Parameters
    ----------
    userId : str
        The unique identifier of the user.
    profileId : str
        The unique identifier of the user's profile.

    Returns
    -------
    Response
        JSON response containing a list of notifications.
    """
    notifications = list(mongo.db.notifications.find())
    enriched_notifications = []

    for notification in notifications:
        notification["_id"] = str(notification["_id"])  # Convert ObjectId to string
        enriched_notifications.append(notification)

    return jsonify(enriched_notifications), 200



@notifications_bp.route("/<string:userId>/profiles/<string:profileId>/notifications", methods=["POST"])
def add_notifications(userId, profileId):
    """
    Add one or more notifications for a specific user profile.

    Parameters
    ----------
    userId : str
        The unique identifier of the user.
    profileId : str
        The unique identifier of the user's profile.

    Request Body
    ------------
    JSON
        A list of notification objects or a single notification object.

    Returns
    -------
    Response
        - 201: Notifications added successfully.
        - 400: Validation error for some or all notifications.
    """
    data = request.json

    # Handle a list of notifications
    if isinstance(data, list):
        errors = []
        for item in data:
            required_fields = ["sender_id", "text"]
            for field in required_fields:
                if field not in item:
                    errors.append({"item": item, "error": f"Missing required field: {field}"})
                    continue


            mongo.db.notifications.insert_one({
                "sender_id": item["sender_id"],
                "text": item["text"],
                "timestamp": item.get("timestamp", None)
            })

        if errors:
            return jsonify({
                "message": "Some notifications were not added",
                "errors": errors
            }), 400

        return jsonify({"message": "Notifications added successfully"}), 201

    # Handle a single notification
    required_fields = ["sender_id", "text"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400


    mongo.db.notifications.insert_one({
        "sender_id": data["sender_id"],
        "is_Checked":False,
        "text": data["text"],
        "timestamp": datetime.utcnow().isoformat()
    })

    return jsonify({"message": "Notification added successfully"}), 201


@notifications_bp.route("/<string:userId>/profiles/<string:profileId>/notifications/<string:notificationId>", methods=["GET"])
def get_single_notification(userId, profileId, notificationId):
    """
    Retrieve a specific notification for a user's profile.

    Parameters
    ----------
    userId : str
        The unique identifier of the user.
    profileId : str
        The unique identifier of the user's profile.
    notificationId : str
        The unique identifier of the notification.

    Returns
    -------
    Response
        - 200: Notification found and returned.
        - 404: Notification not found.
        - 400: Invalid notification ID format.
    """
    try:
        notification_object_id = ObjectId(notificationId)
    except Exception:
        return jsonify({"error": "Invalid notification ID format"}), 400

    notification = mongo.db.notifications.find_one({
        "_id": notification_object_id,
    })

    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    # Convert ObjectId to string for JSON response
    notification["_id"] = str(notification["_id"])

    return jsonify(notification), 200

@notifications_bp.route("/<string:userId>/profiles/<string:profileId>/notifications/<string:notificationId>", methods=["PUT"])
def update_notification(userId, profileId, notificationId):
    """
    Update a specific notification for a user's profile.

    Parameters
    ----------
    userId : str
        The unique identifier of the user.
    profileId : str
        The unique identifier of the user's profile.
    notificationId : str
        The unique identifier of the notification.

    Request Body
    ------------
    JSON
        The fields to update (e.g., text, isChecked).

    Returns
    -------
    Response
        - 200: Notification updated successfully.
        - 404: Notification not found.
        - 400: Invalid notification ID format or missing fields.
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
        {"_id": notification_object_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Notification not found"}), 404

    return jsonify({"message": "Notification updated successfully"}), 200
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
    notification = mongo.db.notifications.find_one({"_id": notification_object_id})
    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    # Elimina la notifica dal database
    mongo.db.notifications.delete_one({"_id": notification_object_id})

    return jsonify({"message": "Notification deleted"}), 204
