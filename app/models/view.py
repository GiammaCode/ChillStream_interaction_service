class View:
    """
    Represents a film view record for a user profile.

    Attributes
    ----------
    filmId :
        The unique identifier of the viewed film.
    userId :
        The unique identifier of the user who owns the profile.
    profileId :
        The unique identifier of the user's profile that viewed the film.
    timesOFTheFilm : int
        The number of times the film has been viewed by the profile.

    Methods
    -------
    to_dict():
        Converts the View instance into a dictionary format.
    """

    def __init__(self, filmId, userId, profileId, timesOFTheFilm: int):
        """
        Initializes a View instance with film, user, profile identifiers, and view count.

        Parameters
        ----------
        filmId : int
            The unique identifier of the viewed film.
        userId : int
            The unique identifier of the user who owns the profile.
        profileId : int
            The unique identifier of the user's profile that viewed the film.
        timesOFTheFilm : int
            The number of times the film has been viewed by the profile.
        """
        self.view_id = str(view_id) if view_id else None
        self.filmId = filmId
        self.userId = userId
        self.profileId = profileId
        self.timesOFTheFilm = timesOFTheFilm

    def to_dict(self):
        """
        Converts the View instance into a dictionary.

        Returns
        -------
        dict
            A dictionary containing the viewed film, user, profile identifiers, and view count.
        """
        return {
            "_id": self.view_id,
            "filmId": self.filmId,
            "userId": self.userId,
            "profileId": self.profileId,
            "timesOFTheFilm": self.timesOFTheFilm,
        }

