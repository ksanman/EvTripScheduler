class User:
    """
    A class used to hold a User from the OSRM request.
    User describes the user who added the charger or media. 
    """
    def __init__(self, ID, profileImageURL=None, reputationPoints=None, username=None):
         self.ID=ID
         self.ProfileImageURL=profileImageURL
         self.ReputationPoints = reputationPoints
         self.Username = username