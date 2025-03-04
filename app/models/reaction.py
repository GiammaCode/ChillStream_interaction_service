from datetime import datetime
from bson import ObjectId

class Reaction:
    """
    Represents a reaction (like, dislike, etc.) from a user profile.
    """

    def __init__(self, filmId,profile_id, type_of_reaction, timestamp=None, reaction_id=None):
        """
        Initializes a Reaction instance.

        Args:
            profile_id (str): The unique MongoDB ObjectId of the profile who reacted.
            type_of_reaction (str): The type of reaction (like, dislike, love, etc.).
            timestamp (str, optional): The time the reaction was made.
            reaction_id (str, optional): The unique ID of the reaction (MongoDB _id).
        """
        self.reaction_id = str(reaction_id) if reaction_id else None
        self.profile_id = str(profile_id)
        self.type_of_reaction = type_of_reaction
        self.timestamp = timestamp if timestamp else datetime.utcnow().isoformat()

    def to_dict(self):
        """
        Converts the Reaction instance into a dictionary.
        """
        return {
            "_id": self.reaction_id,
            "profile_id": self.profile_id,
            "type_of_reaction": self.type_of_reaction,
            "timestamp": self.timestamp
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Reaction instance from a dictionary.
        """
        return Reaction(
            reaction_id=data.get("_id"),
            profile_id=data.get("profile_id"),
            type_of_reaction=data.get("type_of_reaction"),
            timestamp=data.get("timestamp")
        )
