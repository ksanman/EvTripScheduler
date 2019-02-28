class Charger:
    """
    A class used to hold the charger from the OSRM request.
    Charger describes a charging station, including address, type, information about the connection, 
    and any user data (photos, videos, comments).
    """
    def __init__(self, addressInfo, connections, mediaItems = None, userComments = None, dataProviderID=None, dataQualityLevel = None, dateCreated=None,dateLastStatusUpdate=None,
                 dateLastVerified=None,generalComments=None,ID=None,isRecentlyVerified=None,numberOfPoints=None,operatorID=None,statusTypeID=None,submissionStatusTypeID=None,
                 uuid = None, usageCost = None, usageTypeID= None, intersectionLatitude=None, intersectionLongitude=None):
        self.AddressInfo = addressInfo
        self.Connections = connections
        self.DataProviderID = dataProviderID
        self.DataQualityLevel = dataQualityLevel
        self.DateCreated = dateCreated
        self.DateLastStatusUpdate = dateLastStatusUpdate
        self.DateLastVerified = dateLastVerified
        self.GeneralComments = generalComments
        self.ID = ID
        self.IsRecentlyVerified = isRecentlyVerified
        self.MediaItems = mediaItems
        self.NumberOfPoints = numberOfPoints
        self.OperatorID = operatorID
        self.StatusTypeID = statusTypeID
        self.SubmissionStatusTypeID = submissionStatusTypeID
        self.UUID = uuid
        self.UsageCost = usageCost
        self.UsageTypeID = usageTypeID
        self.UserComments = userComments
        self.IntersectionLatitude = intersectionLatitude
        self.IntersectionLongitude = intersectionLongitude