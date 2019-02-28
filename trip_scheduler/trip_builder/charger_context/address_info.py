class AddressInfo:
    """
    A class used to hold the AddressInfo from the OSRM request.
    AddressInfo describes a charger location.
    """
    def __init__(self, accessComments=None, addressLine1=None,addressLine2=None,contactEmail=None,contactTelephone1=None,contactTelephone2=None,
                 countryID=None,distanceUnit=None,ID=None,lat=None,long=None,postcode=None,relatedUrl=None, state=None,title=None,town=None):
            self.AccessComments = accessComments
            self.AddressLine1 = addressLine1
            self.AddressLine2 = addressLine2
            self.ContactEmail = contactEmail
            self.ContactTelephone1 = contactTelephone1
            self.ContactTelephone2 = contactTelephone2
            self.CountryID = countryID
            self.DistanceUnit = distanceUnit
            self.ID = ID
            self.Latitude = lat
            self.Longitude = long
            self.Postcode = postcode
            self.RelatedURL = relatedUrl
            self.StateOrProvince = state
            self.Title = title
            self.Town = town