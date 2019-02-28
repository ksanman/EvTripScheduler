class Connection:
    """
    A class used to hold a Connection from the OSRM request.
    Connection contains information about the chargers connection to the car, such as max voltage, charing speed,
    and charger level.
    """
    def __init__(self, amps=None, connectionTypeId = None, currentTypeId = None, ID = None, levelID = None, powerKw = None, quantity=None, statusTypeID=None, voltage =None):
        self.Amps = amps
        self.ConnectionTypeID = connectionTypeId
        self.CurrentTypeID = currentTypeId
        self.ID = ID
        self.LevelID = levelID
        self.PowerKw = powerKw
        self.Quantity = quantity
        self.StatusTypeID = statusTypeID
        self.Voltage = voltage