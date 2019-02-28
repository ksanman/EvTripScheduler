class UserComment:
    """
    A class used to hold a UserComment from the OSRM request.
    UserComment describes a comment left by a user about the charger.
    """
    def __init__(self,user=None, chargePointsID=None, checkInStatusTypeID=None,commentTypeID=None, dateCreated=None,ID=None,rating=None,userName=None):
        self.ChargePointID = chargePointsID
        self.CheckinStatusTypeID = checkInStatusTypeID
        self.CommentTypeID = commentTypeID
        self.DateCreated = dateCreated
        self.ID = ID
        self.Rating = rating
        self.User=user
        self.UserName=userName