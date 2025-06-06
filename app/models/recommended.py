class Recommended:
    """
    Represents a recommended film for a user profile.

    Attributes
    ----------
    filmId : int
        The unique identifier of the recommended film.
    userId : int
        The unique identifier of the user who owns the profile.
    profileId : int
        The unique identifier of the user's profile for which the recommendation is made.

    Methods
    -------
    to_dict():
        Converts the Recommended instance into a dictionary format.
    """

    def __init__(self, filmId: int, userId: int, profileId: int):
        """
        Initializes a Recommended instance with film, user, and profile identifiers.

        Parameters
        ----------
        filmId : int
            The unique identifier of the recommended film.
        userId : int
            The unique identifier of the user who owns the profile.
        profileId : int
            The unique identifier of the user's profile for which the recommendation is made.
        """
        self.recommended_id = str(recommended_id) if recommended_id else None
        self.filmId = filmId
        self.userId = userId
        self.profileId = profileId

    def to_dict(self):
        """
        Converts the Recommended instance into a dictionary.

        Returns
        -------
        dict
            A dictionary containing the recommended film, user, and profile identifiers.
        """
        return {
            "_id": self.recommended_id,
            "filmId": self.filmId,
            "userId": self.userId,
            "profileId": self.profileId
        }


