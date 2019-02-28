class MediaItem:
    """
    A class used to hold a MediaItem from the OSRM request.
    MediaItem describes a photo or video of the charger.
    """
    def __init__(self, user=None, chargePointID = None, comment = None, dateCreate =None, ID = None, isEnabled = None, isExternalResource = None, isFeaturedItem = None,
                 isVideo=None, itemThumbnailURL = None, itemURL = None):
        self.ChargePointID = chargePointID
        self.Comment = comment
        self.DateCreated = dateCreate
        self.ID = ID
        self.IsEnabled = isEnabled
        self.IsExternalResource = isExternalResource
        self.IsFeaturedItem = isFeaturedItem
        self.IsVideo = isVideo
        self.ItemThumbnailURL = itemThumbnailURL
        self.ItemURL = itemURL
        self.User = user