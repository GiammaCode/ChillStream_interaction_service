from datetime import datetime

from flask import Blueprint, request, jsonify
from bson import ObjectId
from services.db import mongo

# Creazione del Blueprint per le reazioni
reactions_bp = Blueprint("reactions", __name__)

@reactions_bp.route("/<string:userId>/profiles/<string:profileId>/reactions", methods=["GET"])
def get_reactions(userId, profileId):
    """
    Retrieve all reactions made by a specific user profile.

    Args:
        userId (str): The unique MongoDB ObjectId of the user.
        profileId (str): The unique MongoDB ObjectId of the profile.

    Returns:
        Response: A JSON list of reactions or an error message.
    """
    print(f"🔍 DEBUG: Ricevuta richiesta GET per userId: {userId}, profileId: {profileId}")  # Debug

    try:
        user_object_id = ObjectId(userId)
        profile_object_id = ObjectId(profileId)
    except Exception as e:
        return jsonify({"error": "Invalid ID format"}), 400

    reactions = list(mongo.db.reactions.find({"profile_id": profileId}))

    for reaction in reactions:
        reaction["_id"] = str(reaction["_id"])
        reaction["profile_id"] = str(reaction["profile_id"])

    return jsonify({"profile_id": profileId, "reactions": reactions}), 200


@reactions_bp.route("/<string:userId>/profiles/<string:profileId>/reactions", methods=["POST"])
def add_reaction(userId, profileId):
    """
    Add a new reaction for a specific user profile.

    Request Body:
        JSON: { "type_of_reaction": "like" }

    Returns:
        Response: Success message or error message.
    """
    data = request.json

    try:
        user_object_id = ObjectId(userId)
        profile_object_id = ObjectId(profileId)
    except Exception as e:
        return jsonify({"error": "Invalid ID format"}), 400

    reaction_data = {
        "profile_id": profileId,
        "type_of_reaction": data.get("type_of_reaction", ""),
        "timestamp": datetime.utcnow().isoformat()
    }

    result = mongo.db.reactions.insert_one(reaction_data)
    reaction_id = str(result.inserted_id)

    return jsonify({"message": "Reaction added", "reaction_id": reaction_id}), 201

@reactions_bp.route("/<string:userId>/profiles/<string:profileId>/reactions/<string:reactionId>", methods=["DELETE"])
def delete_reaction(userId, profileId, reactionId):
    """
    Delete a specific reaction from a user's profile.

    Returns:
        Response: Success or error message.
    """
    try:
        reaction_object_id = ObjectId(reactionId)
    except Exception as e:
        return jsonify({"error": "Invalid ID format"}), 400

    mongo.db.reactions.delete_one({"_id": reaction_object_id})

    return jsonify({"message": "Reaction deleted"}), 204

